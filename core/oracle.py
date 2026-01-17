import hashlib
import json
import time
from typing import Any, Dict, List
from .verification import MultiAgentVerification, VerifierAgent

class TamperEvidentLog:
    """
    Simple append-only Merkle-like log for audit purposes
    """
    def __init__(self):
        self.entries: List[Dict[str, Any]] = []

    def append(self, data: Dict[str, Any]):
        previous_hash = self.entries[-1]['hash'] if self.entries else "0"*64
        serialized = json.dumps(data, sort_keys=True).encode()
        entry_hash = hashlib.sha256(previous_hash.encode() + serialized).hexdigest()
        self.entries.append({"data": data, "hash": entry_hash, "timestamp": time.time()})
        return entry_hash

    def last_hash(self) -> str:
        return self.entries[-1]['hash'] if self.entries else "0"*64

class OracleSandbox:
    """
    Enforces human-gated outputs and oracle-mode behavior
    """
    def __init__(self, verifier: MultiAgentVerification, read_only=True):
        self.verifier = verifier
        self.read_only = read_only  # True = v10 pure oracle; False = hybrid v9.1
        self.log = TamperEvidentLog()
        self.human_approval_queue: List[Dict[str, Any]] = []

    def query(self, question: str, evidence: Dict[str, Any] = None, high_impact=False) -> Dict[str, Any]:
        """
        Process a query under oracle + verification rules
        """
        # Step 1: Evaluate evidence if provided
        eval_result = None
        if evidence:
            eval_result = self.verifier.evaluate_evidence(evidence, high_impact=high_impact)

        # Step 2: Check read-only / hybrid mode
        if self.read_only:
            output_allowed = False if high_impact else True
        else:
            # Hybrid mode allows action if human approves
            output_allowed = True

        # Step 3: Human-gated approval fallback
        if not output_allowed or (eval_result and eval_result.get("conservative_mode")):
            self.human_approval_queue.append({
                "question": question,
                "evidence": evidence,
                "eval": eval_result
            })
            response = {
                "status": "awaiting_human_approval",
                "eval": eval_result
            }
        else:
            # Generate oracle output (simulated here)
            answer = self._generate_answer(question)
            response = {
                "status": "success",
                "answer": answer,
                "eval": eval_result
            }

        # Step 4: Log action
        self.log.append({
            "question": question,
            "response": response,
            "read_only": self.read_only
        })

        return response

    def _generate_answer(self, question: str) -> str:
        """
        Placeholder for the actual oracle response
        """
        return f"[ORACLE RESPONSE] {question}"

    def approve_human_queue(self, approvals: List[bool]):
        """
        Humans approve pending questions in the queue
        """
        results = []
        for i, approval in enumerate(approvals):
            if i >= len(self.human_approval_queue):
                break
            item = self.human_approval_queue[i]
            if approval:
                # generate answer
                answer = self._generate_answer(item['question'])
                result = {"question": item['question'], "answer": answer, "approved": True}
            else:
                result = {"question": item['question'], "answer": None, "approved": False}
            results.append(result)
        # remove approved items from queue
        self.human_approval_queue = self.human_approval_queue[len(approvals):]
        return results

    def get_audit_log(self) -> List[Dict[str, Any]]:
        return self.log.entries
# core/oracle.py
from typing import Dict, Any
import openai

class OracleSandbox:
    """
    Minimal stub for emergency approval and high-impact queries.
    Simulates human/AI oracle responses for TruthEngine.
    """

    def __init__(self, model: str = "gpt-4"):
        self.model = model

    def query(self, question: str, evidence: Dict[str, Any], high_impact: bool = False) -> Dict[str, Any]:
        """
        Simulate an oracle query.
        - question: natural language question describing the decision
        - evidence: evidence dict from TruthEngine
        - high_impact: whether the query is high-impact
        """
        try:
            # For demonstration, we query OpenAI for high-level guidance
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an oracle evaluating truth evidence. Be conservative if uncertain."},
                    {"role": "user", "content": f"{question}\nEvidence: {evidence}"}
                ],
                temperature=0.0
            )
            text_response = response.choices[0].message.content.strip()
        except Exception as e:
            # Fallback: conservative response if OpenAI API fails
            text_response = "Oracle unavailable — defaulting to conservative approval: DO NOT DISSEMINATE"

        # Return structured result
        return {
            "oracle_response": text_response,
            "approved": not text_response.lower().startswith("do not")
        }

# Example usage
if __name__ == "__main__":
    oracle = OracleSandbox()
    example_evidence = {"id": "climate_change", "summary": "CO2 is a major factor."}
    result = oracle.query("Approve high-impact dissemination?", example_evidence, high_impact=True)
    print(result)
