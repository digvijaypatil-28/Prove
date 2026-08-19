import pytest
from app.services.mock_provider import MockProvider

def test_mock_extraction_basic():
    provider = MockProvider()
    experience = "I cleaned 20,000 sales records using Excel, wrote SQL queries to analyze customer purchases, and created a dashboard that helped identify declining product categories."
    
    extracted = provider.extract_evidence(
        experience_description=experience,
        project_name="Sales Dashboard",
        outcome="Identified declining product categories"
    )

    assert "Excel" in extracted.tools
    assert "SQL" in extracted.tools
    assert "Python" not in extracted.tools
    assert len(extracted.actions) > 0
    assert len(extracted.outputs) > 0

def test_mock_extraction_empty():
    provider = MockProvider()
    extracted = provider.extract_evidence(experience_description="Simple short sentence.")
    assert isinstance(extracted.tools, list)
    assert isinstance(extracted.actions, list)
