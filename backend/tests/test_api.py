import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import init_db

init_db()
client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_analyze_proof_success():
    payload = {
        "target_role": "Junior Data Analyst",
        "target_domain": "Data Analytics",
        "claimed_skills": ["Python", "SQL", "Excel", "Data Analysis"],
        "experience_description": "During my internship, I cleaned around 20,000 sales records using Excel, wrote SQL queries to analyze customer purchases, and created a dashboard that helped identify declining product categories.",
        "project_name": "Sales Analysis Dashboard",
        "outcome": "Identified declining product categories.",
        "evidence_links": "https://github.com/example/sales-analysis",
        "evidence_description": "GitHub repo and report",
        "ai_usage": "AI-assisted"
    }

    response = client.post("/api/proof/analyze", json=payload)
    assert response.status_code == 201
    data = response.json()

    assert data["success"] is True
    assert "record_id" in data
    assert len(data["skill_assessments"]) == 4

    # Verify SQL and Excel are PROVEN
    asm_dict = {a["skill"]: a for a in data["skill_assessments"]}
    assert asm_dict["SQL"]["status"] == "PROVEN"
    assert asm_dict["Excel"]["status"] == "PROVEN"
    assert asm_dict["Python"]["status"] == "CLAIMED"

    # Verify retrieval GET endpoint works
    record_id = data["record_id"]
    get_res = client.get(f"/api/proof/{record_id}")
    assert get_res.status_code == 200
    retrieved_data = get_res.json()
    assert retrieved_data["record_id"] == record_id
    assert retrieved_data["artifact"]["target_role"] == "Junior Data Analyst"

def test_analyze_proof_validation_failure():
    payload = {
        "target_role": "",  # Empty role
        "target_domain": "Data Analytics",
        "claimed_skills": [],  # Empty skills
        "experience_description": "Short",
    }
    response = client.post("/api/proof/analyze", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

def test_build_plan_api():
    payload = {
        "skill_name": "Python",
        "target_role": "Junior Data Analyst",
        "target_domain": "Data Analytics",
        "proof_gap": "No direct Python code provided."
    }
    response = client.post("/api/proof/build", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["skill"] == "Python"
    assert len(data["deliverables"]) > 0
