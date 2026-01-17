from typing import List, Dict, Any
from core.truth_engine import TruthEngine
import openai
import os

# Make sure your API key is set as an environment variable
# e.g., export OPENAI_API_KEY="your_key_here"
openai.api_key = os.getenv("OPENAI_API_KEY")


class Branch:
    """
    A single "branch" of reasoning using the same OpenAI model.
    Each branch has a prompt modifier and a weight.
    """
    def __init__(self, name: str, weight: float, prompt_modifier: str):
        self.name = name
        self.weight = weight
        self.prompt_modifier = prompt_modifier

    def query(self, main_prompt: str, max_tokens=512) -> str:
        """
        Queries OpenAI API with branch-specific instructions
        """
        prompt = f"{self.prompt_modifier}\n{main_prompt}"
        response = openai.ChatCompletion.create(
            model="gpt-4",  # adjust to your preferred model
            messages=[{"role": "system", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.0
        )
        return response['choices'][0]['message']['content'].strip()


class Aggregator:
    """
    Multi-branch aggregator using a single OpenAI agent.
    Weighted aggregation of branch outputs feeds TruthEngine.
    """
    def __init__(self, truth_engine: TruthEngine):
        self.truth_engine = truth_engine
        self.branches: List[Branch] = []

    def add_branch(self, branch: Branch):
        self.branches.append(branch)

    def evaluate(self, main_prompt: str) -> Dict[str, Any]:
        """
        Query all branches, aggregate, and feed TruthEngine
        """
        outputs = []
        for branch in self.branches:
            result = branch.query(main_prompt)
            outputs.append({
                "name": branch.name,
                "weight": branch.weight,
                "response": result
            })

        # Simple weighted aggregation example: concatenate with weights
        aggregated_response = "\n".join([f"[{o['name']}] {o['response']}" for o in outputs])

        # Feed to TruthEngine for evaluation (e.g., capacity/quality metrics)
        self.truth_engine.add_evidence(evidence_id=main_prompt[:30], evidence={
            "prompt": main_prompt,
            "aggregated_response": aggregated_response,
            "branch_outputs": outputs
        })

        return {
            "aggregated_response": aggregated_response,
            "branch_outputs": outputs
        }
