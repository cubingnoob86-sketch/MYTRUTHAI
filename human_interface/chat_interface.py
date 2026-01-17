from agents.openai_agent import OpenAIAgent
from core.oracle import OracleSandbox

class ChatInterface:
    """
    Human-facing conversational interface.
    No autonomous action. No persistence unless approved.
    """

    def __init__(self, agent: OpenAIAgent, oracle: OracleSandbox):
        self.agent = agent
        self.oracle = oracle
        self.chat_history = []

    def chat(self, user_input: str) -> str:
        # Oracle gate (non-high-impact by default)
        oracle_result = self.oracle.query(
            question="Respond to user chat?",
            evidence={"text": user_input},
            high_impact=False
        )

        if oracle_result.get("status") == "denied":
            return "Response withheld by oracle."

        response = self.agent.generate_response(
            prompt=user_input,
            context=self.chat_history
        )

        self.chat_history.append({"user": user_input, "ai": response})
        return response
