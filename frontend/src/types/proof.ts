export interface ExtractedEvidence {
  actions: string[];
  tools: string[];
  outputs: string[];
  outcomes: string[];
}

export interface EvidenceQuality {
  relevance: number;
  depth: number;
  ownership: number;
  outcome: number;
  verifiability: number;
  recency: number;
  transferability: number;
  overall_score: number;
  quality_label: 'Weak' | 'Moderate' | 'Strong' | 'Very Strong';
}

export interface SkillAssessment {
  skill: string;
  status: 'PROVEN' | 'IMPLIED' | 'CLAIMED' | 'UNPROVEN';
  proficiency_level: 'L0' | 'L1' | 'L2' | 'L3' | 'L4' | 'L5';
  proficiency_name: string;
  justification: string;
  proof_gap: string | null;
}

export interface ProofPlan {
  skill: string;
  activity: string;
  why_it_closes_gap: string;
  deliverables: string[];
  evidence: string;
  skills: string[];
  suggested_source: string;
  difficulty: string;
  estimated_effort: string;
}

export interface ProofArtifact {
  record_id: number;
  target_role: string;
  target_domain: string;
  project_title?: string;
  context: string;
  extracted_evidence: ExtractedEvidence;
  claimed_skills: string[];
  skill_assessments: SkillAssessment[];
  evidence_quality: EvidenceQuality;
  proof_plans: ProofPlan[];
  ai_usage: string;
  created_at: string;
}

export interface ProofAnalysisRequest {
  target_role: string;
  target_domain: string;
  claimed_skills: string[];
  experience_description: string;
  project_name?: string;
  project_description?: string;
  outcome?: string;
  evidence_links?: string;
  evidence_description?: string;
  ai_usage?: string;
}

export interface ProofAnalysisResponse {
  success: boolean;
  record_id: number;
  extracted_evidence: ExtractedEvidence;
  skill_assessments: SkillAssessment[];
  evidence_quality: EvidenceQuality;
  proof_plans: ProofPlan[];
  artifact: ProofArtifact;
  created_at: string;
}

export interface ProofBuildPlanRequest {
  proof_record_id?: number;
  skill_name: string;
  target_role: string;
  target_domain: string;
  proof_gap: string;
}
