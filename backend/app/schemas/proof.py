from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from app.schemas.evidence import ExtractedEvidence
from app.schemas.assessment import SkillAssessment, EvidenceQuality, ProofPlan

class ProofAnalysisRequest(BaseModel):
    target_role: str = Field(..., min_length=1, description="Target role e.g. Junior Data Analyst")
    target_domain: str = Field(..., min_length=1, description="Target domain e.g. Data Analytics")
    claimed_skills: List[str] = Field(..., min_length=1, description="List of claimed skills")
    experience_description: str = Field(..., min_length=5, description="User's background/experience text")
    project_name: Optional[str] = None
    project_description: Optional[str] = None
    outcome: Optional[str] = None
    evidence_links: Optional[str] = None
    evidence_description: Optional[str] = None
    ai_usage: Optional[str] = Field("Not specified", description="Not specified | AI-assisted | AI-generated | AI-dependent")

    @field_validator("claimed_skills")
    def validate_skills(cls, v):
        cleaned = [s.strip() for s in v if s and s.strip()]
        if not cleaned:
            raise ValueError("At least one non-empty claimed skill must be provided.")
        return cleaned

class ProofBuildPlanRequest(BaseModel):
    proof_record_id: Optional[int] = None
    skill_name: str = Field(..., min_length=1)
    target_role: str = Field(..., min_length=1)
    target_domain: str = Field(..., min_length=1)
    proof_gap: str = Field(..., min_length=1)

class ProofArtifact(BaseModel):
    record_id: int
    target_role: str
    target_domain: str
    project_title: Optional[str] = None
    context: str
    extracted_evidence: ExtractedEvidence
    claimed_skills: List[str]
    skill_assessments: List[SkillAssessment]
    evidence_quality: EvidenceQuality
    proof_plans: List[ProofPlan]
    ai_usage: str
    created_at: str

class ProofAnalysisResponse(BaseModel):
    success: bool = True
    record_id: int
    extracted_evidence: ExtractedEvidence
    skill_assessments: List[SkillAssessment]
    evidence_quality: EvidenceQuality
    proof_plans: List[ProofPlan]
    artifact: ProofArtifact
    created_at: str
