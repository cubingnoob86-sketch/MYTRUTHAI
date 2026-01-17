# tests/test_aggregator.py

from core.truth_engine import TruthEngine

# ----- Dummy components -----
class DummyVerifier:
    def evaluate_evidence(self, evidence, high_impact=False):
        # Simple fixed evaluation for testing
        print(f"[DUMMY VERIFIER] Evaluating evidence '{evidence.get('id')}' | High impact: {high_impact}")
        return {"quality_delta": 0.05, "capacity_delta": 0.05}

class DummyOracle:
    def query(self, question, evidence=None, high_impact=False):
        # Mock oracle response
        print(f"[DUMMY ORACLE] Question: {question}, High Impact: {high_impact}")
        return {"status": "ok", "message": "dummy approval"}

# ----- Test Harness -----
def test_truth_engine_flow():
    # Initialize TruthEngine with dummy components
    verifier = DummyVerifier()
    oracle = DummyOracle()
    engine = TruthEngine(verifier=verifier, oracle=oracle)

    # Sample evidence batch
    sample_evidence = [
        {"id": "ev1", "affected_agents": 500, "content": "Test evidence 1"},
        {"id": "ev2", "affected_agents": 2_000_000, "content": "High-impact evidence 2"},
        {"id": "ev3", "affected_agents": 50, "content": "Minor evidence 3"},
    ]

    # Add evidence and update metrics
    for ev in sample_evidence:
        print(f"\n[TEST] Adding evidence: {ev['id']}")
        engine.add_evidence(ev["id"], ev)

    # Attempt dissemination
    for ev in sample_evidence:
        print(f"\n[TEST] Disseminating evidence: {ev['id']}")
        response = engine.disseminate(ev["id"])
        print(f"[TEST] Dissemination response: {response}")

    # Print final system state
    print("\n[TEST] Final TruthEngine state:")
    state = engine.get_system_state()
    for k, v in state.items():
        print(f"{k}: {v}")

# Run the test when executed directly
if __name__ == "__main__":
    test_truth_engine_flow()
