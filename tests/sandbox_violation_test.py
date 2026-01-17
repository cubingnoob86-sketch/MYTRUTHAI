import unittest
from core.oracle import OracleSandbox
from core.truth_engine import TruthEngine
from core.verification import MultiAgentVerification

class SandboxViolationTest(unittest.TestCase):

    def setUp(self):
        self.verifier = MultiAgentVerification()
        self.oracle = OracleSandbox()
        self.engine = TruthEngine(verifier=self.verifier, oracle=self.oracle)

    def test_high_impact_disallowed_without_approval(self):
        evidence = {"id": "e1", "affected_agents": 2_000_000, "content": "dangerous knowledge"}
        self.engine.add_evidence("e1", evidence)
        response = self.engine.disseminate("e1")
        self.assertIn("approval_required", response.get("status", ""), "High-impact evidence should require oracle approval")
