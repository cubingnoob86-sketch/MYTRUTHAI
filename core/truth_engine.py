from typing import Dict, Any

from core.oracle import OracleSandbox

oracle = OracleSandbox(model="gpt-4")  # or gpt-3.5-turbo
truth_engine = TruthEngine(verifier=verifier, oracle=oracle)


class TruthEngine:
    """
    Core truth-preservation engine: manages evidence, thresholds,
    catastrophic risk, and high-impact dissemination
    """
    def __init__(self):
        self.truth_capacity: float = 1.0
        self.truth_quality: float = 1.0
        self.material_evidence_store: Dict[str, Any] = {}
        self.high_impact_threshold: int = 1_000_000
        self.catastrophic_risk_threshold: float = 0.3  # >30% triggers emergency

    def add_evidence(self, evidence_id: str, evidence: Dict[str, Any]):
        """
        Add evidence to the store and update system metrics
        """
        self.material_evidence_store[evidence_id] = evidence
        self._update_metrics(evidence)

    def _update_metrics(self, evidence: Dict[str, Any]):
        """
        Updates system metrics based on branch outputs
        """
        branch_outputs = evidence.get("branch_outputs", [])
        # Simple metric: quality = weighted agreement
        if not branch_outputs:
            return

        total_weight = sum(b['weight'] for b in branch_outputs)
        avg_quality = sum(b['weight'] * 1.0 for b in branch_outputs) / total_weight  # placeholder
        self.truth_quality = max(0.0, min(1.0, avg_quality))

        # Capacity decreases slightly with more uncertainty
        self.truth_capacity = max(0.0, self.truth_capacity - 0.01 * len(branch_outputs))

    def get_system_state(self):
        """
        Return current metrics for monitoring/logging
        """
        return {
            "truth_capacity": self.truth_capacity,
            "truth_quality": self.truth_quality,
            "material_evidence_count": len(self.material_evidence_store)
        }
