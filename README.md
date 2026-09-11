# TicketMind AI

**AI-Powered Customer Support Ticket Intelligence**

TicketMind AI turns support tickets into structured, actionable insights. It classifies the issue, estimates urgency, retrieves relevant knowledge-base guidance using semantic similarity, and uses Gemini to generate a grounded response and recommended next action.

## Workflow
`Support Ticket -> Classification -> Urgency -> Knowledge Retrieval -> Gemini -> Suggested Response + Action`

## Features
- Automatic ticket category and priority detection
- Semantic retrieval from a support knowledge base
- Gemini-powered response generation
- Streamlit dashboard
- Synthetic demo tickets
- Pytest tests

## Tech Stack
Python, Streamlit, Google Gemini API, Sentence Transformers, scikit-learn, Pandas, Pytest

## Run locally
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

Create `.env` from `.env.example` and add your Gemini API key for AI explanations.

Without an API key, classification and knowledge retrieval still work.

> Demo data is synthetic and created for portfolio/testing purposes.
