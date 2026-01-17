from typing import Dict, Any, List
import random

class MultiAgentVerification:
    """
    Simplified multi-branch verification system.
    Uses pseudo-independent "agents" (branches) to validate evidence.
    """
    def __init__(self, branches: List[str] = None):
        self.branches = branches or ["analytical", "creative", "conservative"]

    def evaluate_evidence(self, evidence: Dict[str, Any], high_impact: bool = False) -> Dict[str, float]:
        """
        Returns a dict of quality_delta and capacity_delta based on branch agreement.
        """
        branch_outputs = evidence.get("branch_outputs", [])

        if not branch_outputs:
            return {"quality_delta": 0.0, "capacity_delta": 0.0}

        # Compute weighted agreement (simplified)
        total_weight = sum(b.get("weight", 1.0) for b in branch_outputs)
        agreement_score = sum(b.get("weight", 1.0) * random.uniform(0.8, 1.0) for b in branch_outputs) / total_weight

        # Adjust metrics
        quality_delta = (agreement_score - 0.9) * 0.1  # small adjustment
        capacity_delta = -0.01 if high_impact else 0.0

        return {"quality_delta": quality_delta, "capacity_delta": capacity_delta}
