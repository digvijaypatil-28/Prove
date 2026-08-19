import os
import json
import pytest
from app.schemas.proof import ProofAnalysisRequest
from app.services.evidence_extractor import EvidenceExtractor
from app.services.skill_mapper import SkillMapper
from app.services.evidence_scorer import EvidenceScorer
from app.services.proof_gap import ProofGapEngine

EVALUATION_JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "tests",
    "evaluation_cases.json",
)

def load_evaluation_cases():
    if os.path.exists(EVALUATION_JSON_PATH):
        with open(EVALUATION_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@pytest.mark.parametrize("case", load_evaluation_cases(), ids=lambda c: c["id"])
def test_evaluation_case(case):
    input_data = case["input"]
    expected = case["expected"]

    # Handle insufficient text case validation check
    if expected.get("validation_failure_or_claimed"):
        if len(input_data["experience_description"].strip()) < 5:
            with pytest.raises(ValueError):
                ProofAnalysisRequest(**input_data)
            return

    req = ProofAnalysisRequest(**input_data)
    extractor = EvidenceExtractor()
    extracted = extractor.extract(
        experience_description=req.experience_description,
        project_name=req.project_name,
        outcome=req.outcome,
        evidence_description=req.evidence_description,
    )

    mapper = SkillMapper()
    assessments = mapper.map_skills(
        claimed_skills=req.claimed_skills,
        extracted_evidence=extracted,
        has_evidence_links=bool(req.evidence_links and req.evidence_links.strip()),
    )
    asm_dict = {a.skill: a for a in assessments}

    scorer = EvidenceScorer()
    quality = scorer.score_evidence(
        extracted=extracted,
        experience_description=req.experience_description,
        target_role=req.target_role,
        target_domain=req.target_domain,
        evidence_links=req.evidence_links,
        evidence_description=req.evidence_description,
        ai_usage=req.ai_usage,
    )

    gap_engine = ProofGapEngine()
    assessments_with_gaps = gap_engine.identify_gaps(assessments)
    asm_gaps_dict = {a.skill: a for a in assessments_with_gaps}

    # Assertions based on expected dictionary
    if "python_status" in expected:
        assert asm_dict["Python"].status == expected["python_status"]

    if "sql_status" in expected:
        assert asm_dict["SQL"].status == expected["sql_status"]

    if "excel_status" in expected:
        assert asm_dict["Excel"].status == expected["excel_status"]

    if "react_status" in expected:
        assert asm_dict["React"].status == expected["react_status"]

    if "fastapi_status" in expected:
        assert asm_dict["FastAPI"].status == expected["fastapi_status"]

    if "kubernetes_status" in expected:
        assert asm_dict["Kubernetes"].status == expected["kubernetes_status"]

    if "rust_status" in expected:
        assert asm_dict["Rust"].status == expected["rust_status"]

    if "minimum_quality_score" in expected:
        assert quality.overall_score >= expected["minimum_quality_score"]

    if "maximum_quality_score" in expected:
        assert quality.overall_score <= expected["maximum_quality_score"]

    if "quality_label" in expected:
        assert quality.quality_label == expected["quality_label"]

    if "quality_label_in" in expected:
        assert quality.quality_label in expected["quality_label_in"]

    if "python_has_proof_gap" in expected:
        assert asm_gaps_dict["Python"].proof_gap is not None

    if "verifiability_score_max" in expected:
        assert quality.verifiability <= expected["verifiability_score_max"]
