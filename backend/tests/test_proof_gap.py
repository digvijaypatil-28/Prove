import pytest
from app.services.proof_gap import ProofGapEngine
from app.schemas.assessment import SkillAssessment

def test_proof_gap_generation():
    engine = ProofGapEngine()
    assessments = [
        SkillAssessment(
            skill="Python",
            status="CLAIMED",
            proficiency_level="L1",
            proficiency_name="Awareness",
            justification="No Python tools found.",
            proof_gap=None
        ),
        SkillAssessment(
            skill="SQL",
            status="PROVEN",
            proficiency_level="L3",
            proficiency_name="Independent",
            justification="SQL queries verified.",
            proof_gap=None
        )
    ]

    results = engine.identify_gaps(assessments)
    python_asm = [r for r in results if r.skill == "Python"][0]
    sql_asm = [r for r in results if r.skill == "SQL"][0]

    assert python_asm.proof_gap is not None
    assert "Python" in python_asm.proof_gap
    assert sql_asm.proof_gap is None
