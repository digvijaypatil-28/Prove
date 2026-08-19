import pytest
from app.services.evidence_scorer import EvidenceScorer
from app.schemas.evidence import ExtractedEvidence

def test_7_dimension_evidence_scoring():
    scorer = EvidenceScorer()
    extracted = ExtractedEvidence(
        actions=["cleaned dataset using Python", "built automated SQL pipeline"],
        tools=["Python", "SQL", "Git"],
        outputs=["cleaned dataset", "analytical dashboard"],
        outcomes=["improved efficiency by 30%"]
    )

    quality = scorer.score_evidence(
        extracted=extracted,
        experience_description="I built automated data pipelines using Python and SQL.",
        target_role="Data Engineer",
        target_domain="Data Infrastructure",
        evidence_links="https://github.com/example/pipeline",
        evidence_description="GitHub repo with code",
        ai_usage="AI-assisted"
    )

    assert 0 <= quality.relevance <= 100
    assert 0 <= quality.depth <= 100
    assert 0 <= quality.ownership <= 100
    assert 0 <= quality.outcome <= 100
    assert 0 <= quality.verifiability <= 100
    assert 0 <= quality.recency <= 100
    assert 0 <= quality.transferability <= 100
    assert 0 <= quality.overall_score <= 100
    assert quality.quality_label in ["Weak", "Moderate", "Strong", "Very Strong"]

def test_unsupported_numerical_claim_verifiability():
    scorer = EvidenceScorer()
    extracted = ExtractedEvidence(
        actions=[], tools=[], outputs=[], outcomes=["increased sales by 40%"]
    )
    quality = scorer.score_evidence(
        extracted=extracted,
        experience_description="I increased sales by 40%.",
        target_role="Sales Analyst",
        target_domain="Sales",
        evidence_links="",  # No evidence provided
        evidence_description=""
    )
    # Verifiability must be low due to lack of link
    assert quality.verifiability <= 40.0
