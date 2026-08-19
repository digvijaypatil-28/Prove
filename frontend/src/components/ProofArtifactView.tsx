import React, { useState } from 'react';
import { ProofArtifact } from '../types/proof';
import { FileCode, Copy, Check } from 'lucide-react';

interface ProofArtifactViewProps {
  artifact: ProofArtifact;
}

export const ProofArtifactView: React.FC<ProofArtifactViewProps> = ({ artifact }) => {
  const [copied, setCopied] = useState(false);

  const generateMarkdownArtifact = () => {
    return `# PROVE Proof Artifact #${artifact.record_id}

**Target Role**: ${artifact.target_role}  
**Target Domain**: ${artifact.target_domain}  
**AI Usage Declaration**: ${artifact.ai_usage}  
**Created Timestamp**: ${artifact.created_at}  

---

## 1. Candidate Context & Experience
${artifact.context}

---

## 2. Extracted Evidence Facts
- **Actions**: ${artifact.extracted_evidence.actions.join('; ')}
- **Tools**: ${artifact.extracted_evidence.tools.join(', ')}
- **Outputs**: ${artifact.extracted_evidence.outputs.join(', ')}
- **Outcomes**: ${artifact.extracted_evidence.outcomes.join('; ')}

---

## 3. Skill Assessments & Proficiency Levels
${artifact.skill_assessments
  .map(
    (s) =>
      `- **${s.skill}**: status=\`${s.status}\`, level=\`${s.proficiency_level} (${s.proficiency_name})\`  \n  Justification: ${s.justification}${
        s.proof_gap ? `  \n  Proof Gap: ${s.proof_gap}` : ''
      }`
  )
  .join('\n\n')}

---

## 4. Evidence Quality Evaluation
- **Overall Score**: ${artifact.evidence_quality.overall_score} / 100 (${artifact.evidence_quality.quality_label})
- **Relevance**: ${artifact.evidence_quality.relevance}/100 (20%)
- **Depth**: ${artifact.evidence_quality.depth}/100 (15%)
- **Ownership**: ${artifact.evidence_quality.ownership}/100 (15%)
- **Outcome**: ${artifact.evidence_quality.outcome}/100 (15%)
- **Verifiability**: ${artifact.evidence_quality.verifiability}/100 (15%)
- **Recency**: ${artifact.evidence_quality.recency}/100 (10%)
- **Transferability**: ${artifact.evidence_quality.transferability}/100 (10%)

---

## 5. Actionable Proof Plans
${artifact.proof_plans
  .map(
    (p) =>
      `### Skill: ${p.skill}\n- **Activity**: ${p.activity}\n- **Deliverables**: ${p.deliverables.join(
        ', '
      )}\n- **Suggested Source**: ${p.suggested_source}\n- **Effort/Difficulty**: ${p.estimated_effort} (${p.difficulty})`
  )
  .join('\n\n')}
`;
  };

  const handleCopyArtifact = async () => {
    const content = generateMarkdownArtifact();
    await navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  return (
    <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
            <FileCode className="w-5 h-5 text-blue-400" /> Structured Proof Artifact
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">Persisted SQLite Record #{artifact.record_id} • Exportable markdown format</p>
        </div>

        <button
          type="button"
          onClick={handleCopyArtifact}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl font-semibold text-xs text-white bg-blue-600 hover:bg-blue-500 transition shadow-md shadow-blue-500/20 active:scale-95"
        >
          {copied ? (
            <>
              <Check className="w-4 h-4 text-emerald-300" /> Artifact Copied!
            </>
          ) : (
            <>
              <Copy className="w-4 h-4" /> Copy Artifact
            </>
          )}
        </button>
      </div>

      <div className="bg-slate-950/90 rounded-xl p-4 border border-slate-800/80 font-mono text-xs text-slate-300 overflow-x-auto max-h-96">
        <pre className="whitespace-pre-wrap">{generateMarkdownArtifact()}</pre>
      </div>
    </div>
  );
};
