import { ProofAnalysisRequest, ProofAnalysisResponse, ProofBuildPlanRequest, ProofPlan } from '../types/proof';

const API_BASE_URL = 'http://localhost:8000/api';

export async function analyzeProof(data: ProofAnalysisRequest): Promise<ProofAnalysisResponse> {
  const response = await fetch(`${API_BASE_URL}/proof/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `API error (${response.status}): Failed to analyze proof.`);
  }

  return response.json();
}

export async function buildProofPlan(data: ProofBuildPlanRequest): Promise<ProofPlan> {
  const response = await fetch(`${API_BASE_URL}/proof/build`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `API error (${response.status}): Failed to build proof plan.`);
  }

  return response.json();
}

export async function getProofRecord(id: number): Promise<ProofAnalysisResponse> {
  const response = await fetch(`${API_BASE_URL}/proof/${id}`);
  if (!response.ok) {
    throw new Error(`Failed to retrieve proof record #${id}`);
  }
  return response.json();
}

export async function getHealth(): Promise<{ status: string; llm_provider: string; database: string }> {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) {
    throw new Error('Backend health check failed');
  }
  return response.json();
}
