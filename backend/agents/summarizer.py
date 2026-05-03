from .schema import AgentState
import google.generativeai as genai
import json
import os

# Initialize direct Gemini model
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY")))
model = genai.GenerativeModel("gemini-1.5-flash")

def summarize_data(state: AgentState):
    """
    Uses Gemini directly to generate the Morning Briefing narrative based on prioritized items.
    """
    items = state.prioritized_items
    if not items:
        return {"summary": "You're all caught up! No new notifications."}
        
    system_prompt = """
    You are an AI assistant generating a 'Morning Briefing' for a software engineer.
    You will be given a list of prioritized notifications from GitHub and Gmail.
    
    Write a concise, friendly summary (under 3 sentences) grouping related items.
    Focus ONLY on the most important things ("Action Required" or high priority).
    Do not list them out; weave them into a short narrative paragraph.
    Start with a greeting like "Good morning!"
    """
    
    content_to_summarize = json.dumps([
        {
            "tool": item["tool_name"],
            "title": item["title"],
            "priority": item.get("priority_tag", "FYI"),
            "score": item.get("priority_score", 0)
        } for item in items
    ], indent=2)
    
    full_prompt = f"{system_prompt}\n\nNotifications to summarize:\n{content_to_summarize}"
    
    try:
        response = model.generate_content(full_prompt)
        summary_text = response.text.strip()
    except Exception as e:
        print(f"Error in direct summarizer: {e}")
        summary_text = "Failed to generate morning briefing."
        
    return {"summary": summary_text}
