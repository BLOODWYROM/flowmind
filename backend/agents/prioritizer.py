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
    You are an intelligent engineering assistant. Your job is to analyze incoming notifications from GitHub and Gmail.
    For each item, determine:
    1. priority_score (1-10, where 10 is most urgent like production alerts or unblocking a teammate)
    2. priority_tag (Must be one of: "Action Required", "FYI", "Ignore")
    3. ai_explanation (A clear, single-sentence explanation of why it got this score/tag)
    
    Respond ONLY with a JSON array of objects with these keys:
    [
      {"external_id": "...", "priority_score": 8, "priority_tag": "Action Required", "ai_explanation": "..."}
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
