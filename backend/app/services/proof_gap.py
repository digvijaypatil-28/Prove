from typing import List, Optional
from app.schemas.assessment import SkillAssessment

class ProofGapEngine:
    def identify_gaps(self, assessments: List[SkillAssessment]) -> List[SkillAssessment]:
        """
        Ensures every non-proven skill (CLAIMED, IMPLIED, UNPROVEN) has a clear, non-generic proof gap explanation.
        """
        updated = []
        for item in assessments:
            gap = item.proof_gap
            if item.status != "PROVEN" and not gap:
                if item.status == "CLAIMED":
                    gap = (
                        f"No direct code, script, dashboard, or project deliverable was supplied to verify {item.skill}. "
                        f"Construct a hands-on project artifact demonstrating practical implementation of {item.skill}."
                    )
                elif item.status == "IMPLIED":
                    gap = (
                        f"Skill {item.skill} is implied by context, but lacks concrete output deliverables or repository links. "
                        f"Publish an open repository or dataset showing specific execution of {item.skill}."
                    )
                else:  # UNPROVEN
                    gap = f"Insufficient evidence and claim details available for {item.skill}. Supply project details or evidence."

            updated.append(
                SkillAssessment(
                    skill=item.skill,
                    status=item.status,
                    proficiency_level=item.proficiency_level,
                    proficiency_name=item.proficiency_name,
                    justification=item.justification,
                    proof_gap=gap,
                )
            )
        return updated
