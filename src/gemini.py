import os
from dotenv import load_dotenv

load_dotenv()


def generate_response(ticket, analysis, knowledge):
    api_key = os.getenv("GEMINI_API_KEY")
    evidence = "\n\n".join(
        f"[{item['title']}]\n{item['content']}" for item in knowledge
    )

    if not api_key:
        return (
            "### Decision\n"
            f"- Category: **{analysis['category']}**\n"
            f"- Priority: **{analysis['priority']}**\n\n"
            "### Recommended Action\n"
            "Review the ticket against the retrieved knowledge-base guidance "
            "and route it to the appropriate support queue.\n\n"
            "### Note\n"
            "Gemini API key is not configured, so this is the deterministic fallback."
        )

    from google import genai
    client = genai.Client(api_key=api_key)

    prompt = f"""You are a customer-support operations assistant.

Analyze the support ticket using ONLY the ticket, deterministic analysis, and
retrieved knowledge below. Do not invent company policies.

TICKET:
{ticket['text']}

DETERMINISTIC ANALYSIS:
Category: {analysis['category']}
Priority: {analysis['priority']}

RETRIEVED KNOWLEDGE:
{evidence}

Return exactly four short sections:
1. Decision
2. Why this priority
3. Suggested customer response
4. Recommended next action

Clearly distinguish retrieved evidence from your own recommendation.
"""

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt,
    )
    return response.text
