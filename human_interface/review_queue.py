from typing import List, Dict, Any
from core.truth_engine import TruthEngine

class ReviewQueue:
    """
    Holds evidence requiring human review.
    """
    def __init__(self, truth_engine: TruthEngine):
        self.queue: List[Dict[str, Any]] = []
        self.truth_engine = truth_engine

    def add_to_queue(self, evidence_id: str):
        evidence = self.truth_engine.material_evidence_store.get(evidence_id)
        if not evidence:
            return {"status": "error", "message": "Evidence not found"}

        self.queue.append(evidence)
        return {"status": "success", "message": f"Evidence {evidence_id} queued for review"}

    def get_next_for_review(self):
        if not self.queue:
            return None
        return self.queue.pop(0)

    def get_queue_state(self):
        return {"pending_count": len(self.queue)}
