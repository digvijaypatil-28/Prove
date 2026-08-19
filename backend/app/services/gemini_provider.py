import os
import logging
from typing import Optional
from app.services.llm_service import BaseLLMProvider
from app.schemas.evidence import ExtractedEvidence
from app.schemas.assessment import ProofPlan
from app.utils.helpers import parse_json_safely
from app.services.mock_provider import MockProvider

logger = logging.getLogger(__name__)

class GeminiProvider(BaseLLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.mock_fallback = MockProvider()
        self.client = None
        self._init_client()

    def _init_client(self):
        try:
            from google import genai
            self.client = genai.Client(api_key=self.api_key)
            self.mode = "google_genai"
        except Exception:
            try:
                import google.generativeai as legacy_genai
                legacy_genai.configure(api_key=self.api_key)
                self.client = legacy_genai.GenerativeModel("gemini-3.6-flash")
                self.mode = "legacy_genai"
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}. Falling back to MockProvider.")
                self.client = None

    def _load_prompt(self, filename: str) -> str:
        prompt_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "prompts", filename
        )
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def _call_gemini(self, prompt: str) -> str:
        if not self.client:
            raise RuntimeError("Gemini client not initialized")

        models_to_try = ["gemini-3.6-flash"]
        last_err = None

        for model_name in models_to_try:
            try:
                if self.mode == "google_genai":
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                    return response.text
                elif self.mode == "legacy_genai":
                    import google.generativeai as legacy_genai
                    gen_model = legacy_genai.GenerativeModel(model_name)
                    response = gen_model.generate_content(prompt)
                    return response.text
            except Exception as e:
                last_err = e

        raise RuntimeError(f"Gemini API call failed across models: {last_err}")


    def extract_evidence(
        self,
        experience_description: str,
        project_name: Optional[str] = None,
        project_description: Optional[str] = None,
        outcome: Optional[str] = None,
        evidence_description: Optional[str] = None,
    ) -> ExtractedEvidence:
        if not self.client:
            return self.mock_fallback.extract_evidence(
                experience_description, project_name, project_description, outcome, evidence_description
            )

        template = self._load_prompt("extraction_prompt.txt")
        full_text = f"Experience: {experience_description}\n"
        if project_name:
            full_text += f"Project: {project_name}\n"
        if project_description:
            full_text += f"Project Description: {project_description}\n"
        if outcome:
            full_text += f"Outcome: {outcome}\n"
        if evidence_description:
            full_text += f"Evidence Description: {evidence_description}\n"

        prompt = f"{template}\n\nInput Content:\n{full_text}"

        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                raw_response = self._call_gemini(prompt)
                parsed = parse_json_safely(raw_response)
                if parsed:
                    return ExtractedEvidence(
                        actions=parsed.get("actions", []),
                        tools=parsed.get("tools", []),
                        outputs=parsed.get("outputs", []),
                        outcomes=parsed.get("outcomes", []),
                    )
            except Exception as e:
                logger.error(f"Gemini extraction attempt {attempt+1} failed: {e}")

        logger.warning("Gemini extraction failed after retries. Falling back to MockProvider.")
        return self.mock_fallback.extract_evidence(
            experience_description, project_name, project_description, outcome, evidence_description
        )

    def generate_proof_plan(
        self,
        skill: str,
        target_role: str,
        target_domain: str,
        proof_gap: str,
    ) -> ProofPlan:
        if not self.client:
            return self.mock_fallback.generate_proof_plan(skill, target_role, target_domain, proof_gap)

        template = self._load_prompt("proof_builder_prompt.txt")
        prompt = (
            template.replace("{skill}", skill)
            .replace("{target_role}", target_role)
            .replace("{target_domain}", target_domain)
            .replace("{proof_gap}", proof_gap)
        )

        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                raw_response = self._call_gemini(prompt)
                parsed = parse_json_safely(raw_response)
                if parsed:
                    return ProofPlan(
                        skill=skill,
                        activity=parsed.get("activity", f"Build a project demonstrating {skill}"),
                        why_it_closes_gap=parsed.get("why_it_closes_gap", f"Demonstrates hands-on mastery of {skill}"),
                        deliverables=parsed.get("deliverables", ["Source code", "Documentation"]),
                        evidence=parsed.get("evidence", "Public repository and project writeup"),
                        skills=parsed.get("skills", [skill]),
                        suggested_source=parsed.get("suggested_source", "GitHub"),
                        difficulty=parsed.get("difficulty", "Intermediate"),
                        estimated_effort=parsed.get("estimated_effort", "5-10 hours"),
                    )
            except Exception as e:
                logger.error(f"Gemini proof plan attempt {attempt+1} failed: {e}")

        logger.warning("Gemini proof plan generation failed after retries. Falling back to MockProvider.")
        return self.mock_fallback.generate_proof_plan(skill, target_role, target_domain, proof_gap)
