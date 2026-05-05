from .schema import AgentState
from groq import Groq
import json
import os

MODEL = "llama-3.1-8b-instant"

def summarize_data(state: AgentState):
    """
    Uses the Groq API to generate a Morning Briefing from prioritized items.
    """
    _api_key = os.environ.get("GROQ_API_KEY", "")
    try:
        client = Groq(api_key=_api_key)
    except Exception as e:
        print(f"Failed to initialize Groq Client: {e}")
        return {"summary": "Failed to generate morning briefing due to missing API key."}
    
    items = state.prioritized_items
    if not items:
        return {"summary": "You're all caught up! No new notifications."}

    system_prompt = """You are an AI assistant generating a 'Morning Briefing' for a software engineer.
You will be given a list of prioritized notifications from GitHub and Gmail.

Write a concise, friendly summary (under 3 sentences) grouping related items.
Focus ONLY on the most important things ("Action Required" or high priority).
Do not list them out; weave them into a short narrative paragraph.
Start with a greeting like "Good morning!" """

    content_to_summarize = json.dumps([
        {
            "tool": item["tool_name"],
            "title": item["title"],
            "priority": item.get("priority_tag", "FYI"),
            "score": item.get("priority_score", 0)
        } for item in items
    ], indent=2)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Notifications:\n{content_to_summarize}"}
            ]
        )
        summary_text = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in summarizer: {e}")
        summary_text = "Failed to generate morning briefing."

    return {"summary": summary_text}
