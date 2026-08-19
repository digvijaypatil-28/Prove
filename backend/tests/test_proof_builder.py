import pytest
from app.services.proof_builder import ProofBuilderService

def test_proof_builder_plan_generation():
    builder = ProofBuilderService()
    plan = builder.build_plan_for_skill(
        skill="Python",
        target_role="Junior Data Analyst",
        target_domain="Data Analytics",
        proof_gap="No Python code evidence provided."
    )

    assert plan.skill == "Python"
    assert len(plan.deliverables) > 0
    assert plan.activity != ""
    assert plan.why_it_closes_gap != ""
    assert plan.evidence != ""
    assert plan.suggested_source != ""
