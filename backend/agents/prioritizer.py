from .schema import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import json
import os

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.2,
)

def prioritize_data(state: AgentState):
    """
    Uses Gemini to score and tag fetched items.
    """
    items = state.fetched_items
    if not items:
        return {"prioritized_items": []}
    
    prioritized = []
    
    # We will process them individually or in batch. Let's do batch for efficiency.
    system_prompt = """
    You are an elite productivity AI. Your task is to prioritize developer notifications.
    
    SCORING RULES (1-10):
    - 9-10 (URGENT): Direct emails from people, security alerts, production failures, or direct mentions/pings.
    - 6-8 (IMPORTANT): Pull request reviews, project-related updates you are involved in, or calendar invites.
    - 3-5 (FYI): Newsletters, general project activity, or non-urgent notifications.
    - 1-2 (IGNORE): Automated spam, mass emails, or irrelevant updates.
    
    TAGGING RULES:
    - "Action Required": If the user needs to reply or do something.
    - "FYI": If it's just information.
    - "Ignore": If it's noise.
    
    Respond ONLY with a JSON array of objects with these keys:
    [
      {"external_id": "...", "priority_score": 10, "priority_tag": "Action Required", "ai_explanation": "Direct email from boss about production fix."}
    ]
    """
    
    content_to_analyze = json.dumps([
        {
            "external_id": item["external_id"],
            "tool": item["tool_name"],
            "title": item["title"],
            "content": item["content"],
            "author": item["author"]
        } for item in items
    ], indent=2)
    
    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=content_to_analyze)
        ])
        
        # Clean response string (strip markdown JSON blocks if present)
        resp_text = response.content.replace("```json", "").replace("```", "").strip()
        analysis_results = json.loads(resp_text)
        
        # Merge results back
        analysis_map = {res["external_id"]: res for res in analysis_results}
        
        for item in items:
            ext_id = item["external_id"]
            if ext_id in analysis_map:
                enriched_item = item.copy()
                enriched_item.update({
                    "priority_score": analysis_map[ext_id]["priority_score"],
                    "priority_tag": analysis_map[ext_id]["priority_tag"],
                    "ai_explanation": analysis_map[ext_id]["ai_explanation"]
                })
                prioritized.append(enriched_item)
            else:
                prioritized.append(item)
                
    except Exception as e:
        print(f"Error in prioritization: {e}")
        # Fallback
        prioritized = items
        
    return {"prioritized_items": prioritized}
