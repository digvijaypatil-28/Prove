import React, { useEffect, useState } from 'react';
import { Loader2, CheckCircle2, Cpu } from 'lucide-react';

const STEPS = [
  'Extracting structured evidence (Actions, Tools, Outputs, Outcomes)...',
  'Mapping evidence to claimed skills (PROVEN, IMPLIED, CLAIMED, UNPROVEN)...',
  'Calculating L0–L5 proficiency & scoring 7 evidence dimensions...',
  'Identifying proof gaps & generating concrete proof artifact...',
];

export const LoadingProgress: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 600);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="max-w-xl mx-auto py-16 px-6 text-center space-y-6">
      <div className="relative inline-flex items-center justify-center">
        <div className="absolute inset-0 rounded-full bg-blue-500/20 blur-xl animate-pulse"></div>
        <div className="p-4 rounded-2xl glass-panel border border-blue-500/30 text-blue-400 relative">
          <Loader2 className="w-10 h-10 animate-spin" />
        </div>
      </div>

      <div>
        <h3 className="text-xl font-bold text-white tracking-tight">PROVE Intelligence Pipeline Active</h3>
        <p className="text-xs text-slate-400 mt-1 flex items-center justify-center gap-1.5">
          <Cpu className="w-3.5 h-3.5 text-indigo-400" /> Executing extraction, Pydantic validation, scoring & gap analysis
        </p>
      </div>

      <div className="glass-card rounded-2xl p-5 border border-slate-800 text-left space-y-3">
        {STEPS.map((stepText, idx) => {
          const isDone = idx < currentStep;
          const isCurrent = idx === currentStep;

          return (
            <div key={idx} className="flex items-center gap-3 text-xs transition-colors">
              {isDone ? (
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              ) : isCurrent ? (
                <Loader2 className="w-4 h-4 text-blue-400 animate-spin shrink-0" />
              ) : (
                <div className="w-4 h-4 rounded-full border border-slate-700 shrink-0" />
              )}
              <span className={isDone ? 'text-slate-300 font-medium' : isCurrent ? 'text-blue-300 font-semibold' : 'text-slate-500'}>
                {stepText}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
