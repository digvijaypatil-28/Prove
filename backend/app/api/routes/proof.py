import json
import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import (
    ProofRecord,
    ClaimedSkill,
    EvidenceItem,
    SkillAssessmentModel,
    ProofPlanModel,
)
from app.schemas.proof import (
    ProofAnalysisRequest,
    ProofAnalysisResponse,
    ProofBuildPlanRequest,
    ProofArtifact,
)
from app.schemas.assessment import ProofPlan, SkillAssessment, EvidenceQuality
from app.schemas.evidence import ExtractedEvidence

from app.services.evidence_extractor import EvidenceExtractor
from app.services.skill_mapper import SkillMapper
from app.services.evidence_scorer import EvidenceScorer
from app.services.proof_gap import ProofGapEngine
from app.services.proof_builder import ProofBuilderService

router = APIRouter(prefix="/api/proof", tags=["Proof Engine"])

@router.post("/analyze", response_model=ProofAnalysisResponse, status_code=status.HTTP_201_CREATED)
def analyze_proof(req: ProofAnalysisRequest, db: Session = Depends(get_db)):
    """
    Executes full PROVE pipeline:
    Request Validation -> LLM Extraction -> Pydantic Validation -> Skill Mapping ->
    Proficiency Evaluation -> 7-Dimension Evidence Scoring -> Proof Gap Engine ->
    Proof Plan Generation -> SQLite Database Persistence -> Proof Artifact Output
    """
    try:
        # 1. Evidence Extraction
        extractor = EvidenceExtractor()
        extracted = extractor.extract(
            experience_description=req.experience_description,
            project_name=req.project_name,
            project_description=req.project_description,
            outcome=req.outcome,
            evidence_description=req.evidence_description,
        )

        # 2. Skill Mapping & Proficiency (PROVEN/IMPLIED/CLAIMED/UNPROVEN, L0-L5)
        mapper = SkillMapper()
        has_links = bool(req.evidence_links and req.evidence_links.strip())
        assessments = mapper.map_skills(
            claimed_skills=req.claimed_skills,
            extracted_evidence=extracted,
            has_evidence_links=has_links,
        )

        # 3. 7-Dimension Evidence Quality Scoring
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

        # 4. Proof Gap Engine
        gap_engine = ProofGapEngine()
        assessments_with_gaps = gap_engine.identify_gaps(assessments)

        # 5. Proof Plan Generation
        builder = ProofBuilderService()
        proof_plans = builder.build_plans_for_gaps(
            assessments=assessments_with_gaps,
            target_role=req.target_role,
            target_domain=req.target_domain,
        )

        # 6. Database Persistence
        db_record = ProofRecord(
            target_role=req.target_role,
            target_domain=req.target_domain,
            experience_description=req.experience_description,
            project_name=req.project_name,
            project_description=req.project_description,
            outcome=req.outcome,
            evidence_links=req.evidence_links,
            evidence_description=req.evidence_description,
            ai_usage=req.ai_usage or "Not specified",
            created_at=datetime.datetime.utcnow(),
        )
        db.add(db_record)
        db.flush()  # populate db_record.id

        # Save Claimed Skills
        for sk in req.claimed_skills:
            db.add(ClaimedSkill(proof_record_id=db_record.id, skill_name=sk))

        # Save Extracted Evidence & Quality
        db_evidence = EvidenceItem(
            proof_record_id=db_record.id,
            extracted_actions_json=json.dumps(extracted.actions),
            extracted_tools_json=json.dumps(extracted.tools),
            extracted_outputs_json=json.dumps(extracted.outputs),
            extracted_outcomes_json=json.dumps(extracted.outcomes),
            overall_score=quality.overall_score,
            quality_label=quality.quality_label,
            relevance_score=quality.relevance,
            depth_score=quality.depth,
            ownership_score=quality.ownership,
            outcome_score=quality.outcome,
            verifiability_score=quality.verifiability,
            recency_score=quality.recency,
            transferability_score=quality.transferability,
        )
        db.add(db_evidence)

        # Save Skill Assessments
        for asm in assessments_with_gaps:
            db.add(
                SkillAssessmentModel(
                    proof_record_id=db_record.id,
                    skill_name=asm.skill,
                    status=asm.status,
                    proficiency_level=asm.proficiency_level,
                    proficiency_name=asm.proficiency_name,
                    justification=asm.justification,
                    proof_gap=asm.proof_gap,
                )
            )

        # Save Proof Plans
        for plan in proof_plans:
            db.add(
                ProofPlanModel(
                    proof_record_id=db_record.id,
                    skill_name=plan.skill,
                    activity=plan.activity,
                    why_it_closes_gap=plan.why_it_closes_gap,
                    deliverables_json=json.dumps(plan.deliverables),
                    evidence_source=plan.evidence,
                    skills_json=json.dumps(plan.skills),
                    suggested_source=plan.suggested_source,
                    difficulty=plan.difficulty,
                    estimated_effort=plan.estimated_effort,
                )
            )

        db.commit()

        created_iso = db_record.created_at.isoformat()

        # Construct Proof Artifact
        artifact = ProofArtifact(
            record_id=db_record.id,
            target_role=req.target_role,
            target_domain=req.target_domain,
            project_title=req.project_name,
            context=req.experience_description,
            extracted_evidence=extracted,
            claimed_skills=req.claimed_skills,
            skill_assessments=assessments_with_gaps,
            evidence_quality=quality,
            proof_plans=proof_plans,
            ai_usage=req.ai_usage or "Not specified",
            created_at=created_iso,
        )

        return ProofAnalysisResponse(
            success=True,
            record_id=db_record.id,
            extracted_evidence=extracted,
            skill_assessments=assessments_with_gaps,
            evidence_quality=quality,
            proof_plans=proof_plans,
            artifact=artifact,
            created_at=created_iso,
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing proof analysis: {str(e)}",
        )

@router.post("/build", response_model=ProofPlan)
def build_proof_plan(req: ProofBuildPlanRequest, db: Session = Depends(get_db)):
    """
    Generates a targeted Proof Plan to close a specific proof gap for a skill.
    """
    builder = ProofBuilderService()
    plan = builder.build_plan_for_skill(
        skill=req.skill_name,
        target_role=req.target_role,
        target_domain=req.target_domain,
        proof_gap=req.proof_gap,
    )

    if req.proof_record_id:
        db_record = db.query(ProofRecord).filter(ProofRecord.id == req.proof_record_id).first()
        if db_record:
            db_plan = ProofPlanModel(
                proof_record_id=req.proof_record_id,
                skill_name=plan.skill,
                activity=plan.activity,
                why_it_closes_gap=plan.why_it_closes_gap,
                deliverables_json=json.dumps(plan.deliverables),
                evidence_source=plan.evidence,
                skills_json=json.dumps(plan.skills),
                suggested_source=plan.suggested_source,
                difficulty=plan.difficulty,
                estimated_effort=plan.estimated_effort,
            )
            db.add(db_plan)
            db.commit()

    return plan

@router.get("/{id}", response_model=ProofAnalysisResponse)
def get_proof_record(id: int, db: Session = Depends(get_db)):
    """
    Retrieves a persisted Proof Record and constructs its full Proof Artifact.
    """
    record = db.query(ProofRecord).filter(ProofRecord.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Proof Record {id} not found.")

    claimed_skills = [c.skill_name for c in record.claimed_skills]

    ev_item = record.evidence_item
    if ev_item:
        extracted = ExtractedEvidence(
            actions=json.loads(ev_item.extracted_actions_json or "[]"),
            tools=json.loads(ev_item.extracted_tools_json or "[]"),
            outputs=json.loads(ev_item.extracted_outputs_json or "[]"),
            outcomes=json.loads(ev_item.extracted_outcomes_json or "[]"),
        )
        quality = EvidenceQuality(
            relevance=ev_item.relevance_score,
            depth=ev_item.depth_score,
            ownership=ev_item.ownership_score,
            outcome=ev_item.outcome_score,
            verifiability=ev_item.verifiability_score,
            recency=ev_item.recency_score,
            transferability=ev_item.transferability_score,
            overall_score=ev_item.overall_score,
            quality_label=ev_item.quality_label,
        )
    else:
        extracted = ExtractedEvidence()
        quality = EvidenceQuality(
            relevance=0, depth=0, ownership=0, outcome=0,
            verifiability=0, recency=0, transferability=0,
            overall_score=0, quality_label="Weak"
        )

    assessments = [
        SkillAssessment(
            skill=a.skill_name,
            status=a.status,
            proficiency_level=a.proficiency_level,
            proficiency_name=a.proficiency_name,
            justification=a.justification,
            proof_gap=a.proof_gap,
        )
        for a in record.assessments
    ]

    proof_plans = [
        ProofPlan(
            skill=p.skill_name,
            activity=p.activity,
            why_it_closes_gap=p.why_it_closes_gap,
            deliverables=json.loads(p.deliverables_json or "[]"),
            evidence=p.evidence_source,
            skills=json.loads(p.skills_json or "[]"),
            suggested_source=p.suggested_source,
            difficulty=p.difficulty,
            estimated_effort=p.estimated_effort,
        )
        for p in record.proof_plans
    ]

    created_iso = record.created_at.isoformat()

    artifact = ProofArtifact(
        record_id=record.id,
        target_role=record.target_role,
        target_domain=record.target_domain,
        project_title=record.project_name,
        context=record.experience_description,
        extracted_evidence=extracted,
        claimed_skills=claimed_skills,
        skill_assessments=assessments,
        evidence_quality=quality,
        proof_plans=proof_plans,
        ai_usage=record.ai_usage or "Not specified",
        created_at=created_iso,
    )

    return ProofAnalysisResponse(
        success=True,
        record_id=record.id,
        extracted_evidence=extracted,
        skill_assessments=assessments,
        evidence_quality=quality,
        proof_plans=proof_plans,
        artifact=artifact,
        created_at=created_iso,
    )

@router.get("", response_model=List[dict])
def list_proof_records(db: Session = Depends(get_db)):
    """
    Lists all saved proof records with basic metadata.
    """
    records = db.query(ProofRecord).order_by(ProofRecord.id.desc()).limit(50).all()
    result = []
    for r in records:
        result.append({
            "id": r.id,
            "target_role": r.target_role,
            "target_domain": r.target_domain,
            "project_name": r.project_name,
            "claimed_skills": [c.skill_name for c in r.claimed_skills],
            "quality_label": r.evidence_item.quality_label if r.evidence_item else "N/A",
            "overall_score": r.evidence_item.overall_score if r.evidence_item else 0.0,
            "created_at": r.created_at.isoformat(),
        })
    return result
