from typing import Optional
from app.schemas.evidence import ExtractedEvidence
from app.services.llm_service import get_llm_provider

class EvidenceExtractor:
    def __init__(self):
        self.provider = get_llm_provider()

    def extract(
        self,
        experience_description: str,
        project_name: Optional[str] = None,
        project_description: Optional[str] = None,
        outcome: Optional[str] = None,
        evidence_description: Optional[str] = None,
    ) -> ExtractedEvidence:
        extracted = self.provider.extract_evidence(
            experience_description=experience_description,
            project_name=project_name,
            project_description=project_description,
            outcome=outcome,
            evidence_description=evidence_description,
        )
        return extracted
