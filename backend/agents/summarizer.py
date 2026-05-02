from .schema import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import json

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0.4,
)

def summarize_data(state: AgentState):
    """
    Uses Gemini to generate the Morning Briefing narrative based on prioritized items.
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
    
    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=content_to_summarize)
        ])
        
        summary_text = response.content.strip()
    except Exception as e:
        print(f"Error in summarizer: {e}")
        summary_text = "Failed to generate morning briefing."
        
    return {"summary": summary_text}
