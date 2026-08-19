from typing import List, Optional
from pydantic import BaseModel, Field

class EvidenceQuality(BaseModel):
    relevance: float = Field(..., ge=0, le=100)
    depth: float = Field(..., ge=0, le=100)
    ownership: float = Field(..., ge=0, le=100)
    outcome: float = Field(..., ge=0, le=100)
    verifiability: float = Field(..., ge=0, le=100)
    recency: float = Field(..., ge=0, le=100)
    transferability: float = Field(..., ge=0, le=100)
    overall_score: float = Field(..., ge=0, le=100)
    quality_label: str = Field(..., description="Weak | Moderate | Strong | Very Strong")

class SkillAssessment(BaseModel):
    skill: str
    status: str = Field(..., description="PROVEN | IMPLIED | CLAIMED | UNPROVEN")
    proficiency_level: str = Field(..., description="L0 | L1 | L2 | L3 | L4 | L5")
    proficiency_name: str = Field(..., description="Descriptive label for L0-L5")
    justification: str
    proof_gap: Optional[str] = None

class ProofPlan(BaseModel):
    skill: str
    activity: str
    why_it_closes_gap: str
    deliverables: List[str]
    evidence: str
    skills: List[str]
    suggested_source: str
    difficulty: str
    estimated_effort: str
