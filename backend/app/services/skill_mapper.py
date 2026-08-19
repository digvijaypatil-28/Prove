import re
from typing import List, Dict, Any, Tuple
from app.schemas.evidence import ExtractedEvidence
from app.schemas.assessment import SkillAssessment
from app.utils.helpers import normalize_skill_name

SKILL_SYNONYMS: Dict[str, List[str]] = {
    "python": ["python", "pandas", "numpy", "scikit-learn", "py", "pytest", "fastapi", "django", "flask"],
    "sql": ["sql", "queries", "query", "postgresql", "mysql", "sqlite", "sql server", "database"],
    "excel": ["excel", "xlsx", "spreadsheet", "pivot", "xlookup", "vlookup", "csv"],
    "data analysis": ["analysis", "analyzed", "analytics", "data cleaning", "insights", "dashboard", "report"],
    "tableau": ["tableau", "visualization", "dashboard"],
    "power bi": ["power bi", "powerbi", "visualization", "dashboard"],
    "machine learning": ["machine learning", "ml", "scikit-learn", "tensorflow", "pytorch", "model training"],
    "rust": ["rust", "cargo"],
    "go": ["go", "golang"],
}

class SkillMapper:
    def map_skills(
        self,
        claimed_skills: List[str],
        extracted_evidence: ExtractedEvidence,
        has_evidence_links: bool = False,
    ) -> List[SkillAssessment]:
        assessments = []

        all_text = " ".join(
            extracted_evidence.tools +
            extracted_evidence.actions +
            extracted_evidence.outputs +
            extracted_evidence.outcomes
        ).lower()

        tools_lower = [t.lower() for t in extracted_evidence.tools]
        actions_lower = [a.lower() for a in extracted_evidence.actions]
        outputs_lower = [o.lower() for o in extracted_evidence.outputs]
        outcomes_lower = [oc.lower() for oc in extracted_evidence.outcomes]

        for skill in claimed_skills:
            norm_skill = normalize_skill_name(skill)
            status, level, level_name, justification, gap = self._evaluate_single_skill(
                skill=skill,
                norm_skill=norm_skill,
                all_text=all_text,
                tools=tools_lower,
                actions=actions_lower,
                outputs=outputs_lower,
                outcomes=outcomes_lower,
                raw_tools=extracted_evidence.tools,
                raw_actions=extracted_evidence.actions,
                raw_outputs=extracted_evidence.outputs,
                raw_outcomes=extracted_evidence.outcomes,
                has_evidence_links=has_evidence_links,
            )

            assessments.append(
                SkillAssessment(
                    skill=skill,
                    status=status,
                    proficiency_level=level,
                    proficiency_name=level_name,
                    justification=justification,
                    proof_gap=gap,
                )
            )

        return assessments

    def _evaluate_single_skill(
        self,
        skill: str,
        norm_skill: str,
        all_text: str,
        tools: List[str],
        actions: List[str],
        outputs: List[str],
        outcomes: List[str],
        raw_tools: List[str],
        raw_actions: List[str],
        raw_outputs: List[str],
        raw_outcomes: List[str],
        has_evidence_links: bool,
    ) -> Tuple[str, str, str, str, str]:
        synonyms = SKILL_SYNONYMS.get(norm_skill, [norm_skill])

        personal_action_match = False
        team_action_match = False

        for act in actions:
            for syn in synonyms:
                if re.search(r'\b' + re.escape(syn) + r'\b', act):
                    if re.search(r'\b(our company|the team|company|we)\b', act) and not re.search(r'\b(i|my|me)\b', act):
                        team_action_match = True
                    else:
                        personal_action_match = True

        direct_tool_match = any(
            any(re.search(r'\b' + re.escape(syn) + r'\b', tool) for syn in synonyms)
            for tool in tools
        )

        text_mention = any(
            bool(re.search(r'\b' + re.escape(syn) + r'\b', all_text)) for syn in synonyms
        )

        conceptual_support = False
        if norm_skill in ["data analysis", "analytics", "data analytics"]:
            if len(tools) >= 1 and (len(outputs) >= 1 or len(actions) >= 1):
                conceptual_support = True

        if personal_action_match or (direct_tool_match and len(actions) > 0) or conceptual_support:
            status = "PROVEN"
            if has_evidence_links and len(raw_outcomes) > 0:
                level, level_name = "L4", "Advanced / complex application"
            elif (len(raw_outputs) > 0 or len(raw_outcomes) > 0) or has_evidence_links:
                level, level_name = "L3", "Independent practical usage"
            else:
                level, level_name = "L2", "Basic practical usage"

            justification = f"Evidence directly demonstrates personal practical application of {skill} through verified tools and actions."
            gap = None
        elif team_action_match or direct_tool_match or text_mention:
            status = "IMPLIED"
            level, level_name = "L2", "Basic practical usage"
            justification = f"Evidence indirectly mentions {skill} in environment context, but direct personal hands-on execution is ambiguous."
            gap = f"Provide direct personal code or deliverables showcasing hands-on development using {skill}."
        else:
            status = "CLAIMED"
            level, level_name = "L1", "Awareness / basic exposure"
            justification = f"You claimed proficiency in {skill}, but the supplied experience text contains no demonstrated actions, tools, or outputs using {skill}."
            gap = f"No concrete evidence provided for {skill}. Build a dedicated project or supply links/deliverables demonstrating practical usage of {skill}."

        return status, level, level_name, justification, gap

