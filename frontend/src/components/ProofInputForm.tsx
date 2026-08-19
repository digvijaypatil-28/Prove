import React, { useState } from 'react';
import { ProofAnalysisRequest } from '../types/proof';
import { Sparkles, Send, Plus, X, Layers, Code, Link2 } from 'lucide-react';

interface ProofInputFormProps {
  onSubmit: (data: ProofAnalysisRequest) => void;
  isLoading: boolean;
}

export const ProofInputForm: React.FC<ProofInputFormProps> = ({ onSubmit, isLoading }) => {
  const [targetRole, setTargetRole] = useState('');
  const [targetDomain, setTargetDomain] = useState('');
  const [claimedSkills, setClaimedSkills] = useState<string[]>([]);
  const [skillInput, setSkillInput] = useState('');
  const [experienceDescription, setExperienceDescription] = useState('');
  const [projectName, setProjectName] = useState('');
  const [projectDescription, setProjectDescription] = useState('');
  const [outcome, setOutcome] = useState('');
  const [evidenceLinks, setEvidenceLinks] = useState('');
  const [evidenceDescription, setEvidenceDescription] = useState('');
  const [aiUsage, setAiUsage] = useState('AI-assisted');

  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleAddSkill = () => {
    if (skillInput.trim()) {
      const newSkills = skillInput
        .split(',')
        .map((s) => s.trim())
        .filter((s) => s.length > 0 && !claimedSkills.includes(s));
      setClaimedSkills([...claimedSkills, ...newSkills]);
      setSkillInput('');
    }
  };

  const handleRemoveSkill = (skillToRemove: string) => {
    setClaimedSkills(claimedSkills.filter((s) => s !== skillToRemove));
  };

  const handleFillPresetScenario = () => {
    setTargetRole('Junior Data Analyst');
    setTargetDomain('Data Analytics');
    setClaimedSkills(['Python', 'SQL', 'Excel', 'Data Analysis']);
    setExperienceDescription(
      'During my internship, I cleaned around 20,000 sales records using Excel, wrote SQL queries to analyze customer purchases, and created a dashboard that helped identify declining product categories.'
    );
    setProjectName('Sales Analysis Dashboard');
    setProjectDescription('Constructed an analytical sales performance dashboard summarizing customer purchasing patterns.');
    setOutcome('Identified declining product categories.');
    setEvidenceLinks('https://github.com/example/sales-analysis');
    setEvidenceDescription('GitHub repository containing sales dataset, SQL script file, and Excel analysis notebook.');
    setAiUsage('AI-assisted');
    setErrors({});
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!targetRole.trim()) {
      newErrors.targetRole = 'Target role is required.';
    }
    if (!targetDomain.trim()) {
      newErrors.targetDomain = 'Target domain is required.';
    }

    const currentSkills = [...claimedSkills];
    if (skillInput.trim()) {
      const extra = skillInput.split(',').map((s) => s.trim()).filter((s) => s);
      currentSkills.push(...extra);
    }

    if (currentSkills.length === 0) {
      newErrors.claimedSkills = 'At least one claimed skill is required.';
    }

    if (!experienceDescription.trim() || experienceDescription.trim().length < 5) {
      newErrors.experienceDescription = 'Experience description must contain meaningful text (minimum 5 characters).';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    const finalSkills = [...claimedSkills];
    if (skillInput.trim()) {
      const extra = skillInput.split(',').map((s) => s.trim()).filter((s) => s && !finalSkills.includes(s));
      finalSkills.push(...extra);
    }

    onSubmit({
      target_role: targetRole.trim(),
      target_domain: targetDomain.trim(),
      claimed_skills: finalSkills,
      experience_description: experienceDescription.trim(),
      project_name: projectName.trim() || undefined,
      project_description: projectDescription.trim() || undefined,
      outcome: outcome.trim() || undefined,
      evidence_links: evidenceLinks.trim() || undefined,
      evidence_description: evidenceDescription.trim() || undefined,
      ai_usage: aiUsage,
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-6 rounded-2xl glass-panel border border-slate-800">
        <div>
          <h2 className="text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <Layers className="w-6 h-6 text-blue-400" />
            Analyze & Build Proof Artifact
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Input claimed skills and project evidence to extract facts, score evidence quality, and close proof gaps.
          </p>
        </div>
        <button
          type="button"
          onClick={handleFillPresetScenario}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold bg-gradient-to-r from-blue-600/20 to-indigo-600/20 text-blue-300 border border-blue-500/30 hover:border-blue-400/50 transition shadow-sm"
        >
          <Sparkles className="w-4 h-4 text-blue-400" />
          Load Test Scenario
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Required Fields Section */}
        <div className="p-6 rounded-2xl glass-card space-y-5">
          <h3 className="text-sm font-semibold uppercase tracking-wider text-blue-400 flex items-center gap-2">
            <Code className="w-4 h-4" /> 1. Target Role & Claimed Skills (Required)
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">
                Target Role <span className="text-red-400">*</span>
              </label>
              <input
                type="text"
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                placeholder="e.g. Junior Data Analyst"
                className={`w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 ${
                  errors.targetRole ? 'border-red-500/80 focus:ring-red-500/50' : 'border-slate-700 focus:ring-blue-500/50'
                }`}
              />
              {errors.targetRole && <p className="text-xs text-red-400 mt-1">{errors.targetRole}</p>}
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">
                Target Domain <span className="text-red-400">*</span>
              </label>
              <input
                type="text"
                value={targetDomain}
                onChange={(e) => setTargetDomain(e.target.value)}
                placeholder="e.g. Data Analytics"
                className={`w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 ${
                  errors.targetDomain ? 'border-red-500/80 focus:ring-red-500/50' : 'border-slate-700 focus:ring-blue-500/50'
                }`}
              />
              {errors.targetDomain && <p className="text-xs text-red-400 mt-1">{errors.targetDomain}</p>}
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">
              Claimed Skills <span className="text-red-400">*</span>
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={skillInput}
                onChange={(e) => setSkillInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    handleAddSkill();
                  }
                }}
                placeholder="Type a skill (e.g. Python, SQL) and press Enter or comma"
                className="flex-1 px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
              />
              <button
                type="button"
                onClick={handleAddSkill}
                className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold border border-slate-700 transition"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>

            {/* Skill Badges */}
            <div className="flex flex-wrap gap-2 mt-3">
              {claimedSkills.map((skill) => (
                <span
                  key={skill}
                  className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-blue-500/10 border border-blue-500/20 text-blue-300 text-xs font-medium"
                >
                  {skill}
                  <button
                    type="button"
                    onClick={() => handleRemoveSkill(skill)}
                    className="text-blue-400 hover:text-red-400 transition"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                </span>
              ))}
            </div>
            {errors.claimedSkills && <p className="text-xs text-red-400 mt-1">{errors.claimedSkills}</p>}
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">
              Experience Description <span className="text-red-400">*</span>
            </label>
            <textarea
              rows={4}
              value={experienceDescription}
              onChange={(e) => setExperienceDescription(e.target.value)}
              placeholder="Describe what you actually did, tools used, actions performed, and outcomes achieved..."
              className={`w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 ${
                errors.experienceDescription ? 'border-red-500/80 focus:ring-red-500/50' : 'border-slate-700 focus:ring-blue-500/50'
              }`}
            />
            {errors.experienceDescription && <p className="text-xs text-red-400 mt-1">{errors.experienceDescription}</p>}
          </div>
        </div>

        {/* Optional Project & Evidence Section */}
        <div className="p-6 rounded-2xl glass-card space-y-5">
          <h3 className="text-sm font-semibold uppercase tracking-wider text-indigo-400 flex items-center gap-2">
            <Link2 className="w-4 h-4" /> 2. Project Details & Supporting Evidence (Optional)
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Project Name</label>
              <input
                type="text"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                placeholder="e.g. Sales Analysis Dashboard"
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">AI Usage Declaration</label>
              <select
                value={aiUsage}
                onChange={(e) => setAiUsage(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
              >
                <option value="Not specified">Not specified</option>
                <option value="AI-assisted">AI-assisted</option>
                <option value="AI-generated">AI-generated</option>
                <option value="AI-dependent">AI-dependent</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Project Description & Impact Outcome</label>
            <input
              type="text"
              value={outcome}
              onChange={(e) => setOutcome(e.target.value)}
              placeholder="e.g. Identified declining product categories / Reduced latency by 40%"
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Evidence Links (GitHub, Docs, Public Reports)</label>
              <input
                type="text"
                value={evidenceLinks}
                onChange={(e) => setEvidenceLinks(e.target.value)}
                placeholder="https://github.com/username/project"
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Evidence Description</label>
              <input
                type="text"
                value={evidenceDescription}
                onChange={(e) => setEvidenceDescription(e.target.value)}
                placeholder="e.g. Public repo containing dataset and scripts"
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
              />
            </div>
          </div>
        </div>

        {/* Action Button */}
        <div className="flex justify-end pt-2">
          <button
            type="submit"
            disabled={isLoading}
            className="flex items-center gap-2.5 px-7 py-3.5 rounded-xl font-semibold text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 active:scale-[0.98] transition shadow-lg shadow-blue-500/25 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-4 h-4" />
            {isLoading ? 'Analyzing Evidence...' : 'Analyze Evidence'}
          </button>
        </div>
      </form>
    </div>
  );
};
