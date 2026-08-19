from abc import ABC, abstractmethod
from typing import Optional
from app.schemas.evidence import ExtractedEvidence
from app.schemas.assessment import ProofPlan
from app.core.config import settings

class BaseLLMProvider(ABC):
    @abstractmethod
    def extract_evidence(
        self,
        experience_description: str,
        project_name: Optional[str] = None,
        project_description: Optional[str] = None,
        outcome: Optional[str] = None,
        evidence_description: Optional[str] = None,
    ) -> ExtractedEvidence:
        pass

    @abstractmethod
    def generate_proof_plan(
        self,
        skill: str,
        target_role: str,
        target_domain: str,
        proof_gap: str,
    ) -> ProofPlan:
        pass

def get_llm_provider() -> BaseLLMProvider:
    provider_name = settings.LLM_PROVIDER.lower().strip()
    if provider_name == "gemini" and settings.GEMINI_API_KEY:
        from app.services.gemini_provider import GeminiProvider
        return GeminiProvider(api_key=settings.GEMINI_API_KEY)
    else:
        from app.services.mock_provider import MockProvider
        return MockProvider()
