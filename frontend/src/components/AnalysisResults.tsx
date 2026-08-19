import React from 'react';
import { ProofAnalysisResponse } from '../types/proof';
import { Target, Award, ShieldCheck } from 'lucide-react';

interface AnalysisResultsProps {
  data: ProofAnalysisResponse;
}

export const AnalysisResults: React.FC<AnalysisResultsProps> = ({ data }) => {
  const { artifact, evidence_quality, skill_assessments } = data;

  const provenCount = skill_assessments.filter((s) => s.status === 'PROVEN').length;
  const impliedCount = skill_assessments.filter((s) => s.status === 'IMPLIED').length;
  const claimedCount = skill_assessments.filter((s) => s.status === 'CLAIMED').length;

  const getLabelColor = (label: string) => {
    switch (label) {
      case 'Very Strong':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'Strong':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      case 'Moderate':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      default:
        return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
    }
  };

  return (
    <div className="space-y-6">
      {/* Target & Score Overview Header */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Role & Context Card */}
        <div className="md:col-span-2 p-6 rounded-2xl glass-card border border-slate-800 space-y-3">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-blue-400">
            <Target className="w-4 h-4" /> Target Position & Context
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white tracking-tight">{artifact.target_role}</h2>
            <p className="text-xs text-slate-400 mt-0.5">Domain: <span className="text-slate-200 font-medium">{artifact.target_domain}</span></p>
          </div>
          {artifact.project_title && (
            <div className="text-xs text-slate-300 bg-slate-900/60 p-2.5 rounded-xl border border-slate-800">
              <span className="text-slate-400 font-medium">Project:</span> {artifact.project_title}
            </div>
          )}
          <div className="flex flex-wrap gap-2 text-xs pt-1">
            <span className="px-2.5 py-1 rounded-lg bg-slate-800 border border-slate-700 text-slate-300">
              AI Declaration: <strong className="text-white">{artifact.ai_usage}</strong>
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-slate-800 border border-slate-700 text-slate-300">
              Record ID: <strong className="text-blue-400">#{artifact.record_id}</strong>
            </span>
          </div>
        </div>

        {/* Evidence Quality Score Card */}
        <div className="p-6 rounded-2xl glass-card border border-slate-800 flex flex-col justify-between items-center text-center">
          <div className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-indigo-400">
            <Award className="w-4 h-4" /> Evidence Quality
          </div>

          <div className="my-2">
            <div className="text-5xl font-extrabold text-white tracking-tight">
              {evidence_quality.overall_score}
              <span className="text-lg text-slate-500 font-normal">/100</span>
            </div>
            <div className={`mt-2 inline-block px-3 py-1 rounded-full text-xs font-bold border ${getLabelColor(evidence_quality.quality_label)}`}>
              {evidence_quality.quality_label} Quality
            </div>
          </div>

          <div className="w-full grid grid-cols-3 gap-1 pt-2 border-t border-slate-800/80 text-[11px]">
            <div>
              <div className="text-emerald-400 font-bold">{provenCount}</div>
              <div className="text-slate-400">Proven</div>
            </div>
            <div>
              <div className="text-amber-400 font-bold">{impliedCount}</div>
              <div className="text-slate-400">Implied</div>
            </div>
            <div>
              <div className="text-rose-400 font-bold">{claimedCount}</div>
              <div className="text-slate-400">Claimed</div>
            </div>
          </div>
        </div>
      </div>

      {/* Extracted Evidence Fact Chips */}
      <div className="p-6 rounded-2xl glass-card border border-slate-800 space-y-4">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-300 flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-blue-400" /> Extracted Evidence Facts (LLM NLU + Schema Validated)
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          {/* Tools */}
          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
            <div className="font-semibold text-blue-300 uppercase tracking-wider">Verified Tools & Tech</div>
            <div className="flex flex-wrap gap-1.5">
              {data.extracted_evidence.tools.length > 0 ? (
                data.extracted_evidence.tools.map((tool, i) => (
                  <span key={i} className="px-2.5 py-1 rounded-md bg-blue-500/10 text-blue-300 border border-blue-500/20 font-medium">
                    {tool}
                  </span>
                ))
              ) : (
                <span className="text-slate-500 italic">No specific tools extracted</span>
              )}
            </div>
          </div>

          {/* Outputs */}
          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
            <div className="font-semibold text-emerald-300 uppercase tracking-wider">Tangible Deliverables & Outputs</div>
            <div className="flex flex-wrap gap-1.5">
              {data.extracted_evidence.outputs.length > 0 ? (
                data.extracted_evidence.outputs.map((out, i) => (
                  <span key={i} className="px-2.5 py-1 rounded-md bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 font-medium">
                    {out}
                  </span>
                ))
              ) : (
                <span className="text-slate-500 italic">No explicit outputs extracted</span>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2 md:col-span-2">
            <div className="font-semibold text-purple-300 uppercase tracking-wider">Actions Performed</div>
            <ul className="space-y-1 text-slate-300 list-disc list-inside">
              {data.extracted_evidence.actions.map((act, i) => (
                <li key={i}>{act}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
