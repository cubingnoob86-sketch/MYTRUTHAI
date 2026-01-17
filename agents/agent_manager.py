from .claude_agent import ClaudeAgent
from .grok_agent import GrokAgent
from .openai_agent import OpenAIAgent

class AgentManager:
    """
    Wraps multiple AI agents and aggregates their outputs.
    """

    def __init__(self, claude=None, grok=None, openai=None):
        self.agents = [
            claude or ClaudeAgent(),
            grok or GrokAgent(),
            openai or OpenAIAgent()
        ]

    def evaluate_all(self, prompt: str) -> list:
        results = []
        for agent in self.agents:
            res = agent.evaluate(prompt)
            results.append(res)
        return results

    def aggregate(self, results: list) -> dict:
        """
        Simple aggregation: weighted by confidence, fallback to highest-confidence answer.
        Could be replaced by `truth_engine.py` integration.
        """
        filtered = [r for r in results if r["answer"] is not None]
        if not filtered:
            return {"answer": None, "confidence": 0.0, "rationale": "All agents failed", "metadata": {}}

        # naive confidence-weighted selection
        top = max(filtered, key=lambda x: x["confidence"])
        return top
