import React, { useState } from 'react';
import { SkillAssessment, ProofPlan } from '../types/proof';
import { AlertTriangle, Hammer, Loader2, CheckCircle2 } from 'lucide-react';
import { buildProofPlan } from '../services/api';

interface ProofGapSectionProps {
  assessments: SkillAssessment[];
  targetRole: string;
  targetDomain: string;
  recordId: number;
  existingPlans: ProofPlan[];
  onPlanGenerated: (newPlan: ProofPlan) => void;
}

export const ProofGapSection: React.FC<ProofGapSectionProps> = ({
  assessments,
  targetRole,
  targetDomain,
  recordId,
  existingPlans,
  onPlanGenerated,
}) => {
  const gapAssessments = assessments.filter((a) => a.status !== 'PROVEN' && a.proof_gap);
  const [loadingSkill, setLoadingSkill] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleBuildPlan = async (assessment: SkillAssessment) => {
    setLoadingSkill(assessment.skill);
    setErrorMsg(null);
    try {
      const plan = await buildProofPlan({
        proof_record_id: recordId,
        skill_name: assessment.skill,
        target_role: targetRole,
        target_domain: targetDomain,
        proof_gap: assessment.proof_gap || '',
      });
      onPlanGenerated(plan);
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to generate proof plan.');
    } finally {
      setLoadingSkill(null);
    }
  };

  if (gapAssessments.length === 0) {
    return (
      <div className="p-6 rounded-2xl glass-card border border-emerald-500/20 text-center space-y-2">
        <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto" />
        <h3 className="text-base font-bold text-white">No Critical Proof Gaps Identified</h3>
        <p className="text-xs text-slate-300">All claimed skills have direct supporting evidence in the submitted record!</p>
      </div>
    );
  }

  return (
    <div className="p-6 rounded-2xl glass-card border border-slate-800 space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" /> Proof Gap Intelligence Engine
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">Identified evidence deficits with actionable resolution pathways</p>
        </div>
        <span className="text-xs px-2.5 py-1 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 font-semibold">
          {gapAssessments.length} Gap{gapAssessments.length > 1 ? 's' : ''} to Resolve
        </span>
      </div>

      {errorMsg && (
        <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
          {errorMsg}
        </div>
      )}

      <div className="space-y-3">
        {gapAssessments.map((asm) => {
          const hasPlan = existingPlans.some((p) => p.skill.toLowerCase() === asm.skill.toLowerCase());
          const isBuilding = loadingSkill === asm.skill;

          return (
            <div key={asm.skill} className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div className="space-y-1 max-w-2xl text-xs">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-white text-sm">{asm.skill}</span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/10 text-amber-400 border border-amber-500/30 uppercase">
                    {asm.status}
                  </span>
                </div>
                <p className="text-slate-300">{asm.proof_gap}</p>
              </div>

              <button
                type="button"
                onClick={() => handleBuildPlan(asm)}
                disabled={isBuilding}
                className={`px-4 py-2.5 rounded-xl text-xs font-semibold flex items-center gap-2 transition shrink-0 ${
                  hasPlan
                    ? 'bg-emerald-600/20 text-emerald-300 border border-emerald-500/40 hover:bg-emerald-600/30'
                    : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-md shadow-blue-500/20'
                } disabled:opacity-50`}
              >
                {isBuilding ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" /> Building Plan...
                  </>
                ) : (
                  <>
                    <Hammer className="w-4 h-4" /> {hasPlan ? 'Rebuild Proof Plan' : 'Build Proof Plan'}
                  </>
                )}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
};
