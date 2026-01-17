# main.py
import os
import time
from core.truth_engine import TruthEngine
from core.oracle import OracleSandbox
from core.triage import Triage
from agents.openai_agent import OpenAIAgent
from core.utils import load_openai_key

# ----------------------------
# Load API keys
# ----------------------------
OPENAI_API_KEY = load_openai_key("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Set it in your environment variables.")

# ----------------------------
# Instantiate core systems
# ----------------------------
oracle = OracleSandbox(api_key=OPENAI_API_KEY)
truth_engine = TruthEngine(verifier=None, oracle=oracle)  # Replace None if MultiAgentVerification is implemented
triage_system = Triage()  # Handles prioritization of incoming evidence
openai_agent = OpenAIAgent(api_key=OPENAI_API_KEY)

# ----------------------------
# Simulation loop
# ----------------------------
evidence_counter = 1

print("[INFO] TRUTHAL system initialized. Enter 'quit' to stop the loop.")

while True:
    # ------------------------
    # Step 1: Accept new evidence input
    # ------------------------
    content = input("\nEnter evidence content (or 'quit' to exit): ")
    if content.lower() == "quit":
        print("[INFO] Exiting TRUTHAL loop.")
        break

    # Example: number of affected agents is simulated or user-defined
    affected_agents_input = input("Enter number of affected agents (default 1000): ")
    affected_agents = int(affected_agents_input) if affected_agents_input.isdigit() else 1000

    evidence_id = f"evidence_{evidence_counter:03d}"
    evidence_data = {
        "content": content,
        "affected_agents": affected_agents,
        "metadata": {"source": "user_input", "confidence": 0.9}
    }

    # ------------------------
    # Step 2: Add evidence to TruthEngine
    # ------------------------
    print(f"[INFO] Adding evidence {evidence_id}...")
    truth_engine.add_evidence(evidence_id, evidence_data)

    # ------------------------
    # Step 3: Run triage (priority weighting)
    # ------------------------
    prioritized_list = triage_system.rank([evidence_data])
    for ev in prioritized_list:
        # Auto-disseminate based on priority
        response = truth_engine.disseminate(evidence_id)
        print(f"[DISSEMINATION RESPONSE] {response}")

    # ------------------------
    # Step 4: Query agent for verification / summarization
    # ------------------------
    agent_question = f"Summarize and verify: {content}"
    agent_response = openai_agent.query(agent_question)
    print(f"[AGENT RESPONSE] {agent_response}")

    # ------------------------
    # Step 5: Log system state
    # ------------------------
    state = truth_engine.get_system_state()
    print(f"[SYSTEM STATE] {state}")

    evidence_counter += 1
    time.sleep(0.5)  # Prevents console flooding, adjustable
