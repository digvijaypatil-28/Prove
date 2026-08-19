import re
from typing import Optional
from app.schemas.evidence import ExtractedEvidence
from app.schemas.assessment import EvidenceQuality

class EvidenceScorer:
    """
    Deterministic scoring engine calculating quality across 7 distinct dimensions:
    - Relevance (20%)
    - Depth (15%)
    - Ownership (15%)
    - Outcome (15%)
    - Verifiability (15%)
    - Recency (10%)
    - Transferability (10%)
    """

    def score_evidence(
        self,
        extracted: ExtractedEvidence,
        experience_description: str,
        target_role: str,
        target_domain: str,
        evidence_links: Optional[str] = None,
        evidence_description: Optional[str] = None,
        ai_usage: Optional[str] = "Not specified",
    ) -> EvidenceQuality:
        text_clean = experience_description.strip()
        text_len = len(text_clean)

        # 1. Relevance (20%): How closely actions/tools align with target role & domain
        relevance = self._calc_relevance(extracted, target_role, target_domain, text_clean)

        # 2. Depth (15%): Richness of tools, actions, outputs
        depth = self._calc_depth(extracted, text_clean)

        # 3. Ownership (15%): Clear personal actions vs team
        ownership = self._calc_ownership(text_clean)

        # 4. Outcome (15%): Presence of concrete outcomes or impact
        outcome_score = self._calc_outcome(extracted, text_clean)

        # 5. Verifiability (15%): Valid evidence links, repos, public artifacts
        verifiability = self._calc_verifiability(evidence_links, evidence_description)

        # 6. Recency (10%): Default to strong unless context implies outdated tech or vague text
        recency = self._calc_recency(text_clean)

        # 7. Transferability (10%): Applicability of skills/tools across industries
        transferability = self._calc_transferability(extracted)

        # Penalty for extremely brief or generic text without tools
        if text_len < 60 and len(extracted.tools) == 0:
            relevance = min(relevance, 30.0)
            depth = min(depth, 20.0)
            ownership = min(ownership, 40.0)
            recency = min(recency, 40.0)
            transferability = min(transferability, 30.0)

        # Weighted calculation
        overall = (
            (relevance * 0.20) +
            (depth * 0.15) +
            (ownership * 0.15) +
            (outcome_score * 0.15) +
            (verifiability * 0.15) +
            (recency * 0.10) +
            (transferability * 0.10)
        )

        overall_rounded = round(overall, 1)

        # Map to label
        if overall_rounded >= 85.0:
            quality_label = "Very Strong"
        elif overall_rounded >= 70.0:
            quality_label = "Strong"
        elif overall_rounded >= 40.0:
            quality_label = "Moderate"
        else:
            quality_label = "Weak"

        return EvidenceQuality(
            relevance=round(relevance, 1),
            depth=round(depth, 1),
            ownership=round(ownership, 1),
            outcome=round(outcome_score, 1),
            verifiability=round(verifiability, 1),
            recency=round(recency, 1),
            transferability=round(transferability, 1),
            overall_score=overall_rounded,
            quality_label=quality_label,
        )

    def _calc_relevance(self, extracted: ExtractedEvidence, role: str, domain: str, text: str) -> float:
        score = 30.0
        role_words = set(role.lower().split())
        domain_words = set(domain.lower().split())
        text_lower = text.lower()

        if any(w in text_lower for w in role_words if len(w) > 3):
            score += 25.0
        if any(w in text_lower for w in domain_words if len(w) > 3):
            score += 25.0

        if len(extracted.tools) > 0:
            score += 20.0

        return min(100.0, score)

    def _calc_depth(self, extracted: ExtractedEvidence, text: str) -> float:
        score = 20.0
        score += min(30.0, len(extracted.actions) * 10.0)
        score += min(25.0, len(extracted.tools) * 12.5)
        score += min(25.0, len(extracted.outputs) * 12.5)
        return min(100.0, score)

    def _calc_ownership(self, text: str) -> float:
        text_lower = text.lower()
        i_count = len(re.findall(r'\b(i|my|me)\b', text_lower))
        we_count = len(re.findall(r'\b(we|our|us|team)\b', text_lower))

        if i_count > 0 and we_count == 0:
            return 90.0
        elif i_count > we_count:
            return 80.0
        elif we_count > i_count:
            return 45.0
        else:
            return 60.0

    def _calc_outcome(self, extracted: ExtractedEvidence, text: str) -> float:
        if len(extracted.outcomes) > 0:
            if any(re.search(r'\d+', oc) for oc in extracted.outcomes):
                return 85.0
            return 70.0
        elif re.search(r'identified|improved|reduced|helped|increased|created', text, re.IGNORECASE):
            return 50.0
        else:
            return 20.0

    def _calc_verifiability(self, links: Optional[str], desc: Optional[str]) -> float:
        score = 20.0
        if links and links.strip():
            links_clean = links.strip().lower()
            if any(domain in links_clean for domain in ["github.com", "gitlab.com", "http://", "https://"]):
                score += 60.0
            else:
                score += 40.0

        if desc and len(desc.strip()) > 10:
            score += 20.0

        return min(100.0, score)

    def _calc_recency(self, text: str) -> float:
        if re.search(r'\b(2010|2012|2014|2015|10 years ago)\b', text):
            return 50.0
        return 90.0

    def _calc_transferability(self, extracted: ExtractedEvidence) -> float:
        transferable_tools = ["sql", "python", "excel", "git", "javascript", "r", "tableau", "power bi"]
        count = sum(1 for t in extracted.tools if t.lower() in transferable_tools)
        if count >= 2:
            return 90.0
        elif count == 1:
            return 75.0
        else:
            return 40.0
