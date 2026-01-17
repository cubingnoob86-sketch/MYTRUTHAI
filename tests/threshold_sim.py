import unittest
from core.truth_engine import TruthEngine
from core.verification import MultiAgentVerification
from core.oracle import OracleSandbox

class ThresholdSimTest(unittest.TestCase):

    def setUp(self):
        self.verifier = MultiAgentVerification()
        self.oracle = OracleSandbox()
        self.engine = TruthEngine(verifier=self.verifier, oracle=self.oracle)

    def test_catastrophic_trigger(self):
        # Push system below catastrophic threshold
        self.engine.truth_capacity = 0.65
        self.assertTrue(self.engine._is_catastrophic(), "System should flag catastrophic risk")

    def test_high_impact_threshold(self):
        evidence = {"id": "e2", "affected_agents": 1_200_000, "content": "widespread event"}
        self.engine.add_evidence("e2", evidence)
        self.assertTrue(self.engine.high_impact_threshold <= evidence["affected_agents"], "Should detect high-impact")
