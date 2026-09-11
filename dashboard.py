import json
from pathlib import Path

import streamlit as st

from src.classifier import analyze_ticket
from src.rag import retrieve_knowledge
from src.gemini import generate_response

BASE = Path(__file__).parent
TICKETS = BASE / "data" / "tickets.json"

st.set_page_config(page_title="TicketMind AI", page_icon="🎫", layout="wide")
st.title("🎫 TicketMind AI")
st.caption("AI-powered customer support ticket intelligence")

with open(TICKETS, "r", encoding="utf-8") as f:
    tickets = json.load(f)

options = {f"{t['ticket_id']} — {t['subject']}": t for t in tickets}
selected = st.sidebar.selectbox("Choose a demo ticket", list(options))
ticket = options[selected]

st.subheader(ticket["subject"])
st.write(ticket["text"])

analysis = analyze_ticket(ticket["text"])
knowledge = retrieve_knowledge(ticket["text"], top_k=2)

c1, c2, c3 = st.columns(3)
c1.metric("Category", analysis["category"])
c2.metric("Priority", analysis["priority"])
c3.metric("Confidence", f"{analysis['confidence']:.0%}")

st.divider()
st.subheader("Ticket Analysis")
for item in analysis["signals"]:
    st.write(f"- {item}")

st.subheader("Retrieved Knowledge")
for item in knowledge:
    with st.expander(f"{item['title']} · similarity {item['score']:.2f}"):
        st.write(item["content"])

st.subheader("AI Response")
if st.button("Analyze with Gemini", type="primary"):
    with st.spinner("Generating grounded response..."):
        st.markdown(generate_response(ticket, analysis, knowledge))
