from typing import List, Optional
from app.schemas.assessment import ProofPlan, SkillAssessment
from app.services.llm_service import get_llm_provider

class ProofBuilderService:
    def __init__(self):
        self.provider = get_llm_provider()

    def build_plan_for_skill(
        self,
        skill: str,
        target_role: str,
        target_domain: str,
        proof_gap: str,
    ) -> ProofPlan:
        return self.provider.generate_proof_plan(
            skill=skill,
            target_role=target_role,
            target_domain=target_domain,
            proof_gap=proof_gap,
        )

    def build_plans_for_gaps(
        self,
        assessments: List[SkillAssessment],
        target_role: str,
        target_domain: str,
    ) -> List[ProofPlan]:
        plans = []
        for assessment in assessments:
            if assessment.status != "PROVEN" and assessment.proof_gap:
                plan = self.build_plan_for_skill(
                    skill=assessment.skill,
                    target_role=target_role,
                    target_domain=target_domain,
                    proof_gap=assessment.proof_gap,
                )
                plans.append(plan)
        return plans
