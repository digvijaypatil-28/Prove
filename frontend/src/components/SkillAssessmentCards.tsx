import React from 'react';
import { SkillAssessment } from '../types/proof';
import { CheckCircle2, HelpCircle, AlertCircle, AlertTriangle, Layers } from 'lucide-react';

interface SkillAssessmentCardsProps {
  assessments: SkillAssessment[];
}

export const SkillAssessmentCards: React.FC<SkillAssessmentCardsProps> = ({ assessments }) => {
  const getStatusBadge = (status: SkillAssessment['status']) => {
    switch (status) {
      case 'PROVEN':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
            <CheckCircle2 className="w-3.5 h-3.5" /> PROVEN
          </span>
        );
      case 'IMPLIED':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold bg-amber-500/10 text-amber-400 border border-amber-500/30">
            <HelpCircle className="w-3.5 h-3.5" /> IMPLIED
          </span>
        );
      case 'CLAIMED':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold bg-rose-500/10 text-rose-400 border border-rose-500/30">
            <AlertCircle className="w-3.5 h-3.5" /> CLAIMED ONLY
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold bg-slate-500/10 text-slate-400 border border-slate-500/30">
            UNPROVEN
          </span>
        );
    }
  };

  const getProficiencyColor = (level: string) => {
    switch (level) {
      case 'L5':
      case 'L4':
        return 'bg-emerald-500';
      case 'L3':
        return 'bg-blue-500';
      case 'L2':
        return 'bg-amber-500';
      default:
        return 'bg-rose-500';
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
          <Layers className="w-5 h-5 text-blue-400" /> Skill Evidence Assessments & L0–L5 Proficiency
        </h3>
        <span className="text-xs text-slate-400">{assessments.length} skills analyzed</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {assessments.map((asm, idx) => (
          <div key={idx} className="p-5 rounded-2xl glass-card border border-slate-800 space-y-3 flex flex-col justify-between">
            <div className="space-y-2">
              <div className="flex items-center justify-between gap-2">
                <h4 className="text-lg font-bold text-white tracking-tight">{asm.skill}</h4>
                {getStatusBadge(asm.status)}
              </div>

              {/* Proficiency Level Bar */}
              <div className="space-y-1">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-400 font-medium">Proficiency Level</span>
                  <span className="text-slate-200 font-semibold">{asm.proficiency_level} — {asm.proficiency_name}</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden flex gap-0.5 p-0.5">
                  {['L0', 'L1', 'L2', 'L3', 'L4', 'L5'].map((lvl, index) => {
                    const activeLevelNum = parseInt(asm.proficiency_level.replace('L', ''), 10);
                    const isActive = index <= activeLevelNum && activeLevelNum > 0;

                    return (
                      <div
                        key={lvl}
                        className={`h-full flex-1 rounded-sm transition-all ${
                          isActive ? getProficiencyColor(asm.proficiency_level) : 'bg-slate-700/50'
                        }`}
                      />
                    );
                  })}
                </div>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed pt-1">{asm.justification}</p>
            </div>

            {asm.proof_gap && (
              <div className="p-3 rounded-xl bg-amber-500/5 border border-amber-500/20 text-xs space-y-1">
                <div className="font-semibold text-amber-400 flex items-center gap-1.5">
                  <AlertTriangle className="w-3.5 h-3.5" /> Proof Gap Identified
                </div>
                <p className="text-amber-200/90 leading-normal">{asm.proof_gap}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
