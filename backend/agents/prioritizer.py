from .schema import AgentState
import google.generativeai as genai
import json
import os
import re
import traceback

# Initialize LLM directly with google-generativeai
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY")))
model = genai.GenerativeModel("gemini-1.5-flash")

def prioritize_data(state: AgentState):
    """
    Uses Gemini directly to score and tag fetched items in a single bulk API call.
    """
    items = state.fetched_items
    if not items:
        return {"prioritized_items": []}
    
    prioritized = []
    
    system_prompt = """You are an expert prioritization AI.
Analyze the provided items (emails/notifications) and score their importance from 1-10.

Rules:
- 9-10: Urgent action needed (deadlines, emergencies, direct requests)
- 7-8: Important, needs response soon (work updates, opportunities)
- 5-6: Good to know but not urgent (updates, newsletters from people you know)
- 3-4: Low priority (automated notifications, social updates)
- 1-2: Can ignore (promotional emails, spam, bulk newsletters)

Respond ONLY with a valid JSON object mapping the 'external_id' of each item to its score.
Example format:
{
  "id_123": {
    "priority_score": 8,
    "priority_tag": "Action Required",
    "ai_explanation": "This email contains an urgent deadline."
  },
  "id_456": {
    "priority_score": 2,
    "priority_tag": "Can Ignore",
    "ai_explanation": "This is a generic newsletter."
  }
}"""
    
    # Create the payload of items to analyze
    payload = []
    for item in items:
        payload.append({
            "external_id": item["external_id"],
            "tool": item.get("tool_name", "unknown"),
            "subject": item.get("title", "No Subject"),
            "sender": item.get("author", "Unknown"),
            "body_preview": item.get("content", "")[:300]
        })
        
    human_content = json.dumps(payload, indent=2)
    full_prompt = f"{system_prompt}\n\nItems to analyze:\n{human_content}"
    
    try:
        print(f"GEMINI KEY EXISTS: {bool(os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY'))}")
        print(f"Prioritizing {len(items)} items in ONE bulk direct API call...")
        
        response = model.generate_content(full_prompt)
        resp_text = response.text.strip()
        
        # Extract JSON dictionary block
        match = re.search(r'\{.*\}', resp_text, re.DOTALL)
        if match:
            try:
                analysis_map = json.loads(match.group(0))
                print(f"Successfully parsed AI scores for {len(analysis_map)} items.")
                
                for item in items:
                    ext_id = item["external_id"]
                    if ext_id in analysis_map:
                        res = analysis_map[ext_id]
                        item["priority_score"] = int(res.get("priority_score", 0))
                        item["priority_tag"] = res.get("priority_tag", "FYI")
                        item["ai_explanation"] = res.get("ai_explanation", "Analyzed by AI")
                    else:
                        item["priority_score"] = 0
                        item["priority_tag"] = "Can Ignore"
                        item["ai_explanation"] = "AI missed this item"
                        
                    prioritized.append(item)
                    
            except Exception as parse_e:
                print(f"JSON Parse Error: {parse_e}")
                print(f"Raw Response: {resp_text}")
                prioritized = items
        else:
            print(f"No JSON dictionary found. Raw: {resp_text}")
            prioritized = items
            
    except Exception as e:
        print(f"Error in direct prioritization: {str(e)}")
        print(traceback.format_exc())
        prioritized = items
        
    return {"prioritized_items": prioritized}
