import React from 'react';
import { ProofPlan } from '../types/proof';
import { Hammer, CheckSquare, Clock, Share2 } from 'lucide-react';

interface ProofBuilderSectionProps {
  plans: ProofPlan[];
}

export const ProofBuilderSection: React.FC<ProofBuilderSectionProps> = ({ plans }) => {
  if (plans.length === 0) return null;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
          <Hammer className="w-5 h-5 text-emerald-400" /> Actionable Proof Plans
        </h3>
        <span className="text-xs text-slate-400">{plans.length} plan{plans.length > 1 ? 's' : ''} constructed</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {plans.map((plan, idx) => (
          <div key={idx} className="p-5 rounded-2xl glass-card border border-slate-800 space-y-4 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center justify-between gap-2 border-b border-slate-800 pb-2">
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">Proof Blueprint: {plan.skill}</span>
                <div className="flex items-center gap-1.5 text-[11px]">
                  <span className="px-2 py-0.5 rounded bg-blue-500/10 text-blue-300 border border-blue-500/20 font-medium">
                    {plan.difficulty}
                  </span>
                  <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 font-medium flex items-center gap-1">
                    <Clock className="w-3 h-3 text-slate-400" /> {plan.estimated_effort}
                  </span>
                </div>
              </div>

              <div>
                <h4 className="text-sm font-bold text-white leading-snug">{plan.activity}</h4>
                <p className="text-xs text-slate-300 mt-1 italic">{plan.why_it_closes_gap}</p>
              </div>

              <div className="space-y-1.5 pt-1">
                <div className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                  <CheckSquare className="w-3.5 h-3.5 text-blue-400" /> Expected Deliverables
                </div>
                <ul className="space-y-1 text-xs text-slate-300 list-disc list-inside bg-slate-900/60 p-3 rounded-xl border border-slate-800">
                  {plan.deliverables.map((item, dIdx) => (
                    <li key={dIdx}>{item}</li>
                  ))}
                </ul>
              </div>

              <div className="text-xs space-y-1">
                <span className="text-slate-400 font-medium flex items-center gap-1">
                  <Share2 className="w-3.5 h-3.5 text-indigo-400" /> Proof Source Venue:
                </span>
                <span className="text-white font-semibold bg-slate-800 px-2.5 py-1 rounded-lg inline-block border border-slate-700">
                  {plan.suggested_source} ({plan.evidence})
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
