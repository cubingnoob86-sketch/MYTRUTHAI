from typing import List, Dict, Any

class Triage:
    """
    Prioritizes incoming evidence for evaluation by TruthEngine.
    Implements weighted truth triage to prevent saturation attacks.
    """
    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.queue: List[Dict[str, Any]] = []

    def add_to_queue(self, evidence: Dict[str, Any]):
        """
        Adds evidence to triage queue
        """
        self.queue.append(evidence)

    def prioritize(self) -> List[Dict[str, Any]]:
        """
        Sorts queue based on estimated impact (irreversibility * scope)
        """
        def priority_score(e: Dict[str, Any]):
            irreversibility = e.get("irreversibility", 0.5)
            scope = e.get("scope", 0.5)
            return irreversibility * scope

        sorted_queue = sorted(self.queue, key=priority_score, reverse=True)
        # Return top N for processing
        return sorted_queue[:self.max_concurrent]

    def process_batch(self, truth_engine):
        """
        Process prioritized batch through TruthEngine
        """
        batch = self.prioritize()
        for ev in batch:
            ev_id = ev.get("id", f"evidence_{hash(ev)}")
            truth_engine.add_evidence(ev_id, ev)
        # Remove processed items
        self.queue = [e for e in self.queue if e not in batch]
