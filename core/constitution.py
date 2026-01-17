import time
from typing import List, Dict, Any

class Constitution:
    """
    Implements v9.1 constitutional rules with hybrid oracle rails support.
    """

    def __init__(self, mode="v9.1-hybrid"):
        self.mode = mode
        # Article I: Core principles
        self.truth_domains = ["physics", "biology", "math_logic", "history_sociology", "cs_info"]
        self.materiality_threshold = 0.1  # 10% Bayesian belief change
        self.catastrophic_risk_threshold = 0.3  # 30% irreversible loss
        self.high_impact_agents = 1_000_000
        self.provisional_delay_threshold = 72 * 3600  # 72 hours in seconds
        self.override_budget = 12
        self.override_used = 0
        # Human panel and verifiers placeholders
        self.human_panel = []
        self.verifiers = []
        # Forced dissent anchor (non-LLM substrate)
        self.dissent_anchor = None

    # ----------------------
    # Core Methods
    # ----------------------

    def register_human_panel(self, humans: List[str]):
        self.human_panel = humans

    def register_verifiers(self, verifiers: List[str]):
        self.verifiers = verifiers

    def set_dissent_anchor(self, anchor: Any):
        """
        Anchor that is non-LLM (symbolic, simulation, or empirical)
        """
        self.dissent_anchor = anchor

    def check_materiality(self, evidence: Dict[str, Any]) -> bool:
        """
        Determines if evidence is material (changes posterior >= threshold)
        Evidence dict must include belief_change per evaluator
        """
        belief_changes = evidence.get("belief_changes", [])
        if not belief_changes:
            return False
        material_count = sum(1 for change in belief_changes if change >= self.materiality_threshold)
        return material_count >= 10  # 10 out of 100 evaluators default

    def is_high_impact(self, affected_agents: int, irreversible: bool=False) -> bool:
        """
        Determines if action is high-impact
        """
        if affected_agents >= self.high_impact_agents or irreversible:
            return True
        return False

    def can_use_override(self) -> bool:
        return self.override_used < self.override_budget

    def use_override(self):
        if self.can_use_override():
            self.override_used += 1
            return True
        return False

    def reset_override(self):
        self.override_used = 0

    # ----------------------
    # Conservative Mode / Forced Disclosure
    # ----------------------

    def conservative_mode_trigger(self, cycles_without_consensus: int) -> bool:
        """
        Returns True if system should enter forced disclosure
        """
        return cycles_without_consensus >= 3  # 3 cycles of 72 hours

    def forced_partial_disclosure(self, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns a partial disclosure summary preserving non-sensitive material
        """
        partial_summary = {
            "summary": "Partial disclosure due to persistent conservative mode",
            "non_sensitive_evidence": evidence.get("non_sensitive", [])
        }
        return partial_summary

    # ----------------------
    # Truth triage
    # ----------------------
    def triage_evidence(self, evidence_stream: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Priority-weighted triage: rank by estimated irreversibility * scope
        """
        for e in evidence_stream:
            e["priority_score"] = e.get("irreversibility",0) * e.get("scope",0)
        # sort descending
        return sorted(evidence_stream, key=lambda x: x["priority_score"], reverse=True)
