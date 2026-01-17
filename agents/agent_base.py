from abc import ABC, abstractmethod

class AgentBase(ABC):
    """
    Base interface for all AI minds.
    """

    @abstractmethod
    def evaluate(self, prompt: str) -> dict:
        """
        Evaluate a prompt and return structured output.
        Must include:
            - 'answer': str
            - 'confidence': float (0-1)
            - 'rationale': str
            - 'metadata': dict
        """
        pass
