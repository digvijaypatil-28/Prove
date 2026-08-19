import React from 'react';
import { ShieldCheck, Cpu, Database } from 'lucide-react';

interface HeaderProps {
  llmProvider: string;
  onReset: () => void;
  hasResults: boolean;
}

export const Header: React.FC<HeaderProps> = ({ llmProvider, onReset, hasResults }) => {
  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-800/80 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3 cursor-pointer" onClick={onReset}>
          <div className="bg-gradient-to-tr from-blue-600 to-indigo-500 p-2.5 rounded-xl shadow-lg shadow-blue-500/20">
            <ShieldCheck className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white">PROVE</h1>
              <span className="text-xs px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-medium">
                v1.0 MVP
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">Proof Builder & Evidence Intelligence Engine</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-xs">
            <Cpu className="w-3.5 h-3.5 text-indigo-400" />
            <span className="text-slate-400">LLM Mode:</span>
            <span className="font-semibold text-slate-200 uppercase">{llmProvider || 'mock'}</span>
          </div>

          <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-xs">
            <Database className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-emerald-400 font-medium">SQLite Active</span>
          </div>

          {hasResults && (
            <button
              onClick={onReset}
              className="px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 transition border border-slate-700"
            >
              Start New Analysis
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
