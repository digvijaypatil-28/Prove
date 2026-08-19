import re
from typing import Optional, List
from app.services.llm_service import BaseLLMProvider
from app.schemas.evidence import ExtractedEvidence
from app.schemas.assessment import ProofPlan

KNOWN_TOOLS = [
    "excel", "sql", "python", "pandas", "numpy", "tableau", "power bi", "powerbi",
    "r", "sql server", "postgresql", "mysql", "docker", "git", "github", "jira",
    "javascript", "typescript", "react", "fastapi", "django", "flask", "aws", "gcp",
    "azure", "spark", "hadoop", "scikit-learn", "tensorflow", "pytorch"
]

ACTION_VERBS = [
    "cleaned", "built", "wrote", "analyzed", "created", "developed", "designed",
    "automated", "implemented", "managed", "optimized", "calculated", "trained",
    "deployed", "configured", "processed", "migrated", "extracted", "transformed"
]

class MockProvider(BaseLLMProvider):
    def extract_evidence(
        self,
        experience_description: str,
        project_name: Optional[str] = None,
        project_description: Optional[str] = None,
        outcome: Optional[str] = None,
        evidence_description: Optional[str] = None,
    ) -> ExtractedEvidence:
        combined_text = f"{experience_description} {project_description or ''} {outcome or ''} {evidence_description or ''}"
        text_lower = combined_text.lower()

        # Extract Tools
        extracted_tools = []
        for tool in KNOWN_TOOLS:
            # Pattern match whole word
            if re.search(r'\b' + re.escape(tool) + r'\b', text_lower):
                # Standardize display casing
                display_name = tool.upper() if tool in ["sql", "r", "aws", "gcp"] else tool.title()
                if display_name not in extracted_tools:
                    extracted_tools.append(display_name)

        # Extract Actions
        extracted_actions = []
        sentences = re.split(r'[.!?;\n]+', combined_text)
        for sentence in sentences:
            sentence_clean = sentence.strip()
            if not sentence_clean:
                continue
            words = sentence_clean.lower().split()
            if any(verb in words for verb in ACTION_VERBS):
                # Keep concise action phrase
                if len(sentence_clean) > 80:
                    extracted_actions.append(sentence_clean[:80] + "...")
                else:
                    extracted_actions.append(sentence_clean)

        if not extracted_actions and combined_text.strip():
            extracted_actions.append("Described relevant practical domain background")

        # Extract Outputs
        extracted_outputs = []
        output_keywords = ["dashboard", "dataset", "query", "queries", "report", "model", "script", "pipeline", "app", "application", "repository", "codebase"]
        for kw in output_keywords:
            if kw in text_lower:
                if kw in ["query", "queries"]:
                    extracted_outputs.append("SQL analytical queries")
                elif kw == "dashboard":
                    extracted_outputs.append("Analytical visualization dashboard")
                elif kw == "dataset":
                    extracted_outputs.append("Cleaned analytical dataset")
                elif kw in ["report", "model", "script", "pipeline"]:
                    extracted_outputs.append(f"Domain {kw}")

        # Extract Outcomes
        extracted_outcomes = []
        if outcome and outcome.strip():
            extracted_outcomes.append(outcome.strip())

        outcome_phrases = re.findall(r'(helped [^.!\n]+|identified [^.!\n]+|increased [^.!\n]+|reduced [^.!\n]+|improved [^.!\n]+|saved [^.!\n]+|resulted in [^.!\n]+)', combined_text, re.IGNORECASE)
        for ph in outcome_phrases:
            clean_ph = ph.strip()
            if clean_ph not in extracted_outcomes:
                extracted_outcomes.append(clean_ph)

        # Deduplicate
        extracted_tools = list(dict.fromkeys(extracted_tools))
        extracted_actions = list(dict.fromkeys(extracted_actions))
        extracted_outputs = list(dict.fromkeys(extracted_outputs))
        extracted_outcomes = list(dict.fromkeys(extracted_outcomes))

        return ExtractedEvidence(
            actions=extracted_actions,
            tools=extracted_tools,
            outputs=extracted_outputs,
            outcomes=extracted_outcomes,
        )

    def generate_proof_plan(
        self,
        skill: str,
        target_role: str,
        target_domain: str,
        proof_gap: str,
    ) -> ProofPlan:
        skill_norm = skill.strip().lower()
        if "python" in skill_norm:
            return ProofPlan(
                skill=skill,
                activity=f"Build an end-to-end {target_domain} data processing pipeline using Python and Pandas.",
                why_it_closes_gap="Demonstrates direct, verifiable Python programming capability and data manipulation proficiency.",
                deliverables=[
                    "Python data cleaning script (.py)",
                    "Exploratory Data Analysis Jupyter Notebook (.ipynb)",
                    "Cleaned dataset & findings summary",
                    "GitHub Repository with detailed README"
                ],
                evidence="Public GitHub repository containing tested Python scripts, sample data, and execution logs.",
                skills=[skill, "Data Cleaning", "Pandas", "Git"],
                suggested_source="GitHub & Kaggle",
                difficulty="Intermediate",
                estimated_effort="6-10 hours"
            )
        elif "sql" in skill_norm:
            return ProofPlan(
                skill=skill,
                activity=f"Construct an analytical SQL benchmark suite for a {target_domain} database.",
                why_it_closes_gap="Provides transparent code evidence of advanced SQL queries, joins, aggregations, and window functions.",
                deliverables=[
                    "SQL schema definition script (.sql)",
                    "Complex query suite (CTEs, joins, window functions)",
                    "Query execution benchmark report"
                ],
                evidence="GitHub repository or DB Fiddle containing reproducible SQL scripts.",
                skills=[skill, "Database Design", "Analytical Querying"],
                suggested_source="GitHub / DB Fiddle",
                difficulty="Intermediate",
                estimated_effort="4-6 hours"
            )
        elif "excel" in skill_norm:
            return ProofPlan(
                skill=skill,
                activity="Create an interactive Excel financial/operations dashboard with automated macros & pivot models.",
                why_it_closes_gap="Proves capability in Excel formulas, XLOOKUP, pivot tables, and dashboard design.",
                deliverables=[
                    "Interactive Excel Workbook (.xlsx)",
                    "Executive Summary PDF",
                    "Video walkthrough demonstrating dynamic formulas"
                ],
                evidence="Downloadable sample workbook on GitHub or Google Drive with video demonstration link.",
                skills=[skill, "Pivot Tables", "VBA/Macros", "Data Visualization"],
                suggested_source="GitHub / Loom",
                difficulty="Beginner to Intermediate",
                estimated_effort="3-5 hours"
            )
        else:
            return ProofPlan(
                skill=skill,
                activity=f"Implement a hands-on {target_domain} capstone project focusing on {skill} for the role of {target_role}.",
                why_it_closes_gap=f"Closes the gap by creating verifiable proof of {skill} in a real-world scenario.",
                deliverables=[
                    f"Project repository demonstrating {skill}",
                    "Technical documentation & architecture diagram",
                    "Project execution report"
                ],
                evidence=f"Published GitHub project repository & live documentation page.",
                skills=[skill, "Technical Documentation", "Problem Solving"],
                suggested_source="GitHub & Technical Blog",
                difficulty="Intermediate",
                estimated_effort="8-12 hours"
            )
