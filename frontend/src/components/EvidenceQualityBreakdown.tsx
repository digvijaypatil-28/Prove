import React from 'react';
import { EvidenceQuality } from '../types/proof';
import { Award } from 'lucide-react';

interface EvidenceQualityBreakdownProps {
  quality: EvidenceQuality;
}

export const EvidenceQualityBreakdown: React.FC<EvidenceQualityBreakdownProps> = ({ quality }) => {
  const dimensions = [
    { name: 'Relevance', score: quality.relevance, weight: '20%', desc: 'Alignment of skills & tools with target role & domain' },
    { name: 'Depth', score: quality.depth, weight: '15%', desc: 'Richness & specificity of actions, tools, and outputs' },
    { name: 'Ownership', score: quality.ownership, weight: '15%', desc: 'Personal responsibility vs team effort' },
    { name: 'Outcome', score: quality.outcome, weight: '15%', desc: 'Presence of concrete measurable business/tech outcomes' },
    { name: 'Verifiability', score: quality.verifiability, weight: '15%', desc: 'Public repositories, links, or verifiable artifacts' },
    { name: 'Recency', score: quality.recency, weight: '10%', desc: 'Timeliness of demonstrated skills' },
    { name: 'Transferability', score: quality.transferability, weight: '10%', desc: 'Broad applicability of skills across industries' },
  ];

  const getBarColor = (score: number) => {
    if (score >= 80) return 'bg-emerald-500';
    if (score >= 60) return 'bg-blue-500';
    if (score >= 40) return 'bg-amber-500';
    return 'bg-rose-500';
  };

  return (
    <div className="p-6 rounded-2xl glass-card border border-slate-800 space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
            <Award className="w-5 h-5 text-indigo-400" /> 7-Dimension Evidence Quality Breakdown
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">Transparent weighted scoring system (Deterministic Python Engine)</p>
        </div>
        <div className="text-right">
          <div className="text-xl font-extrabold text-white">{quality.overall_score}<span className="text-xs text-slate-400 font-normal">/100</span></div>
          <div className="text-xs font-semibold text-indigo-400">{quality.quality_label} Quality</div>
        </div>
      </div>

      <div className="space-y-3.5">
        {dimensions.map((dim) => (
          <div key={dim.name} className="space-y-1 text-xs">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-slate-200">{dim.name}</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
                  Weight: {dim.weight}
                </span>
              </div>
              <span className="font-bold text-white">{dim.score.toFixed(1)} / 100</span>
            </div>

            <div className="w-full bg-slate-800/80 h-2.5 rounded-full overflow-hidden p-0.5 border border-slate-700/50">
              <div
                className={`h-full rounded-full transition-all duration-500 ${getBarColor(dim.score)}`}
                style={{ width: `${Math.min(100, Math.max(0, dim.score))}%` }}
              />
            </div>

            <p className="text-[11px] text-slate-400 italic">{dim.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
