import { useEffect, useState } from 'react';
import { ProofAnalysisRequest, ProofAnalysisResponse, ProofPlan } from './types/proof';
import { analyzeProof, getHealth } from './services/api';
import { Header } from './components/Header';
import { ProofInputForm } from './components/ProofInputForm';
import { LoadingProgress } from './components/LoadingProgress';
import { AnalysisResults } from './components/AnalysisResults';
import { SkillAssessmentCards } from './components/SkillAssessmentCards';
import { EvidenceQualityBreakdown } from './components/EvidenceQualityBreakdown';
import { ProofGapSection } from './components/ProofGapSection';
import { ProofBuilderSection } from './components/ProofBuilderSection';
import { ProofArtifactView } from './components/ProofArtifactView';
import { AlertCircle, RefreshCw } from 'lucide-react';

export default function App() {
  const [llmProvider, setLlmProvider] = useState('mock');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [lastRequest, setLastRequest] = useState<ProofAnalysisRequest | null>(null);

  const [analysisResult, setAnalysisResult] = useState<ProofAnalysisResponse | null>(null);
  const [proofPlans, setProofPlans] = useState<ProofPlan[]>([]);

  useEffect(() => {
    getHealth()
      .then((data) => {
        setLlmProvider(data.llm_provider || 'mock');
      })
      .catch(() => {
        setLlmProvider('mock');
      });
  }, []);

  const handleAnalyze = async (requestData: ProofAnalysisRequest) => {
    setIsLoading(true);
    setErrorMsg(null);
    setLastRequest(requestData);

    try {
      const response = await analyzeProof(requestData);
      setAnalysisResult(response);
      setProofPlans(response.proof_plans || []);
    } catch (err: any) {
      setErrorMsg(err.message || 'An error occurred while connecting to the PROVE backend.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    if (lastRequest) {
      handleAnalyze(lastRequest);
    }
  };

  const handleReset = () => {
    setAnalysisResult(null);
    setProofPlans([]);
    setErrorMsg(null);
    setLastRequest(null);
  };

  const handlePlanGenerated = (newPlan: ProofPlan) => {
    setProofPlans((prev) => {
      const filtered = prev.filter((p) => p.skill.toLowerCase() !== newPlan.skill.toLowerCase());
      return [...filtered, newPlan];
    });

    if (analysisResult) {
      setAnalysisResult({
        ...analysisResult,
        artifact: {
          ...analysisResult.artifact,
          proof_plans: [...analysisResult.artifact.proof_plans.filter((p) => p.skill.toLowerCase() !== newPlan.skill.toLowerCase()), newPlan],
        },
      });
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-blue-500 selection:text-white">
      <Header llmProvider={llmProvider} onReset={handleReset} hasResults={!!analysisResult} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-8">
        {isLoading && <LoadingProgress />}

        {errorMsg && !isLoading && (
          <div className="max-w-xl mx-auto my-12 p-6 rounded-2xl bg-rose-500/10 border border-rose-500/30 space-y-4 text-center">
            <AlertCircle className="w-10 h-10 text-rose-400 mx-auto" />
            <div>
              <h3 className="text-lg font-bold text-white">Analysis Request Failed</h3>
              <p className="text-xs text-rose-300 mt-1">{errorMsg}</p>
            </div>
            <div className="flex items-center justify-center gap-3 pt-2">
              <button
                type="button"
                onClick={handleRetry}
                className="flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-rose-600 hover:bg-rose-500 text-white transition shadow-md"
              >
                <RefreshCw className="w-3.5 h-3.5" /> Retry Request
              </button>
              <button
                type="button"
                onClick={handleReset}
                className="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 transition border border-slate-700"
              >
                Reset Form
              </button>
            </div>
          </div>
        )}

        {!isLoading && !errorMsg && !analysisResult && (
          <ProofInputForm onSubmit={handleAnalyze} isLoading={isLoading} />
        )}

        {!isLoading && !errorMsg && analysisResult && (
          <div className="space-y-8 animate-fadeIn">
            <AnalysisResults data={analysisResult} />

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 space-y-6">
                <SkillAssessmentCards assessments={analysisResult.skill_assessments} />
                <ProofGapSection
                  assessments={analysisResult.skill_assessments}
                  targetRole={analysisResult.artifact.target_role}
                  targetDomain={analysisResult.artifact.target_domain}
                  recordId={analysisResult.record_id}
                  existingPlans={proofPlans}
                  onPlanGenerated={handlePlanGenerated}
                />
                <ProofBuilderSection plans={proofPlans} />
              </div>

              <div className="space-y-6">
                <EvidenceQualityBreakdown quality={analysisResult.evidence_quality} />
              </div>
            </div>

            <ProofArtifactView artifact={{ ...analysisResult.artifact, proof_plans: proofPlans }} />
          </div>
        )}
      </main>

      <footer className="border-t border-slate-900 py-6 text-center text-xs text-slate-500 glass-panel mt-12">
        <p>PROVE — Proof Builder & Evidence Intelligence • Deterministic Scoring & Fact-Grounded LLM NLU</p>
      </footer>
    </div>
  );
}
