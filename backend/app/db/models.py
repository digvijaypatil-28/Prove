import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    proof_records = relationship("ProofRecord", back_populates="user")

class ProofRecord(Base):
    __tablename__ = "proof_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    target_role = Column(String(255), nullable=False)
    target_domain = Column(String(255), nullable=False)
    experience_description = Column(Text, nullable=False)
    project_name = Column(String(255), nullable=True)
    project_description = Column(Text, nullable=True)
    outcome = Column(Text, nullable=True)
    evidence_links = Column(Text, nullable=True)
    evidence_description = Column(Text, nullable=True)
    ai_usage = Column(String(50), nullable=True, default="Not specified")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="proof_records")
    claimed_skills = relationship("ClaimedSkill", back_populates="proof_record", cascade="all, delete-orphan")
    evidence_item = relationship("EvidenceItem", back_populates="proof_record", uselist=False, cascade="all, delete-orphan")
    assessments = relationship("SkillAssessmentModel", back_populates="proof_record", cascade="all, delete-orphan")
    proof_plans = relationship("ProofPlanModel", back_populates="proof_record", cascade="all, delete-orphan")

class ClaimedSkill(Base):
    __tablename__ = "claimed_skills"

    id = Column(Integer, primary_key=True, index=True)
    proof_record_id = Column(Integer, ForeignKey("proof_records.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(255), nullable=False)

    proof_record = relationship("ProofRecord", back_populates="claimed_skills")

class EvidenceItem(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)
    proof_record_id = Column(Integer, ForeignKey("proof_records.id", ondelete="CASCADE"), nullable=False, unique=True)
    extracted_actions_json = Column(Text, nullable=False)  # JSON string list
    extracted_tools_json = Column(Text, nullable=False)    # JSON string list
    extracted_outputs_json = Column(Text, nullable=False)  # JSON string list
    extracted_outcomes_json = Column(Text, nullable=False) # JSON string list

    overall_score = Column(Float, nullable=False)
    quality_label = Column(String(50), nullable=False)
    relevance_score = Column(Float, nullable=False)
    depth_score = Column(Float, nullable=False)
    ownership_score = Column(Float, nullable=False)
    outcome_score = Column(Float, nullable=False)
    verifiability_score = Column(Float, nullable=False)
    recency_score = Column(Float, nullable=False)
    transferability_score = Column(Float, nullable=False)

    proof_record = relationship("ProofRecord", back_populates="evidence_item")

class SkillAssessmentModel(Base):
    __tablename__ = "skill_assessments"

    id = Column(Integer, primary_key=True, index=True)
    proof_record_id = Column(Integer, ForeignKey("proof_records.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)            # PROVEN, IMPLIED, CLAIMED, UNPROVEN
    proficiency_level = Column(String(10), nullable=False)  # L0, L1, L2, L3, L4, L5
    proficiency_name = Column(String(100), nullable=False) # e.g. Independent practical usage
    justification = Column(Text, nullable=False)
    proof_gap = Column(Text, nullable=True)

    proof_record = relationship("ProofRecord", back_populates="assessments")

class ProofPlanModel(Base):
    __tablename__ = "proof_plans"

    id = Column(Integer, primary_key=True, index=True)
    proof_record_id = Column(Integer, ForeignKey("proof_records.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(255), nullable=False)
    activity = Column(Text, nullable=False)
    why_it_closes_gap = Column(Text, nullable=False)
    deliverables_json = Column(Text, nullable=False)      # JSON string list
    evidence_source = Column(Text, nullable=False)
    skills_json = Column(Text, nullable=False)           # JSON string list
    suggested_source = Column(String(255), nullable=False)
    difficulty = Column(String(50), nullable=False)
    estimated_effort = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    proof_record = relationship("ProofRecord", back_populates="proof_plans")
