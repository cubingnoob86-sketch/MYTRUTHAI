import unittest
from core.truth_engine import TruthEngine
from core.verification import MultiAgentVerification
from core.oracle import OracleSandbox
from human_interface.review_queue import ReviewQueue

class TriageTest(unittest.TestCase):

    def setUp(self):
        self.verifier = MultiAgentVerification()
        self.oracle = OracleSandbox()
        self.engine = TruthEngine(verifier=self.verifier, oracle=self.oracle)
        self.review_queue = ReviewQueue(truth_engine=self.engine)

    def test_queue_addition(self):
        evidence = {"id": "e3", "affected_agents": 2_000_000, "content": "disputed"}
        self.engine.add_evidence("e3", evidence)
        self.review_queue.add_to_queue("e3")
        self.assertEqual(len(self.review_queue.queue), 1, "Evidence should be queued for review")

    def test_queue_retrieval(self):
        evidence = {"id": "e4", "affected_agents": 1_500_000, "content": "needs review"}
        self.engine.add_evidence("e4", evidence)
        self.review_queue.add_to_queue("e4")
        next_item = self.review_queue.get_next_for_review()
        self.assertEqual(next_item["id"], "e4", "Next item in queue should match added evidence")
