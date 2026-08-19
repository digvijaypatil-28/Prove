import pytest
from app.services.skill_mapper import SkillMapper
from app.schemas.evidence import ExtractedEvidence

def test_skill_mapping_proven_and_claimed():
    mapper = SkillMapper()
    claimed = ["Python", "SQL", "Excel", "Data Analysis"]
    
    # Evidence has SQL and Excel, but NO Python
    evidence = ExtractedEvidence(
        actions=["cleaned 20,000 sales records using Excel", "wrote SQL queries"],
        tools=["Excel", "SQL"],
        outputs=["analytical dashboard", "sales dataset"],
        outcomes=["identified declining product categories"]
    )

    assessments = mapper.map_skills(claimed_skills=claimed, extracted_evidence=evidence)
    
    assessment_dict = {a.skill: a for a in assessments}

    # Verify SQL and Excel are PROVEN
    assert assessment_dict["SQL"].status == "PROVEN"
    assert assessment_dict["Excel"].status == "PROVEN"
    
    # Verify Python is CLAIMED (NOT falsely marked PROVEN)
    assert assessment_dict["Python"].status == "CLAIMED"
    assert assessment_dict["Python"].proficiency_level == "L1"
    assert "No concrete evidence provided for Python" in assessment_dict["Python"].proof_gap

def test_skill_mapping_implied():
    mapper = SkillMapper()
    claimed = ["Rust"]
    evidence = ExtractedEvidence(
        actions=["worked during backend services migration"],
        tools=["Python"],
        outputs=[],
        outcomes=[]
    )

    assessments = mapper.map_skills(claimed_skills=claimed, extracted_evidence=evidence)
    assert assessments[0].status == "CLAIMED"
