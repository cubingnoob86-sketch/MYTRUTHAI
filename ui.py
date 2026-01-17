import streamlit as st
from core.truth_engine import TruthEngine
from core.oracle import OracleSandbox
from agents.openai_agent import OpenAIAgent
from human_interface.chat_interface import ChatInterface
from agents.openai_agent import OpenAIAgent
from core.oracle import OracleSandbox

# Init
agent = OpenAIAgent(api_key="YOUR_OPENAI_KEY")
oracle = OracleSandbox()
chat = ChatInterface(agent, oracle)

st.header("Chat with TRUTHAL")

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

user_msg = st.text_input("You:", "")

if st.button("Send"):
    ai_msg = chat.chat(user_msg)
    st.session_state.chat_log.append((user_msg, ai_msg))

for u, a in st.session_state.chat_log:
    st.markdown(f"**You:** {u}")
    st.markdown(f"**TRUTHAL:** {a}")

# Initialize components
oracle = OracleSandbox()
truth_engine = TruthEngine(oracle=oracle)
agent = OpenAIAgent(api_key="YOUR_OPENAI_KEY")  # replace with your OpenAI key

st.title("TRUTHAL AI Interface")

# Sidebar: add new evidence
st.sidebar.header("Add Evidence")
evidence_id = st.sidebar.text_input("Evidence ID")
description = st.sidebar.text_area("Description")
affected_agents = st.sidebar.number_input("Affected Agents", min_value=0, value=0)

if st.sidebar.button("Submit Evidence"):
    evidence = {
        "id": evidence_id,
        "description": description,
        "affected_agents": affected_agents,
        "source": "user"
    }
    truth_engine.add_evidence(evidence_id, evidence)
    st.sidebar.success(f"Evidence '{evidence_id}' added.")

# Main panel: list stored evidence
st.header("Material Evidence")
for eid, ev in truth_engine.material_evidence_store.items():
    st.write(f"ID: {eid}, Desc: {ev['description']}, Agents: {ev['affected_agents']}")

# Disseminate evidence
st.header("Disseminate Evidence")
eid_to_disseminate = st.selectbox("Select evidence to disseminate", list(truth_engine.material_evidence_store.keys()))
if st.button("Disseminate"):
    result = truth_engine.disseminate(eid_to_disseminate)
    st.success(f"Dissemination result: {result}")

# Show system state
st.header("System State")
state = truth_engine.get_system_state()
st.json(state)
