from .schema import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import json
import os

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.2,
)

def prioritize_data(state: AgentState):
    """
    Uses Gemini to score and tag fetched items individually for higher accuracy.
    """
    items = state.fetched_items
    if not items:
        return {"prioritized_items": []}
    
    prioritized = []
    
    # Create individual prompts for each item
    prompts = []
    for item in items:
        system_prompt = """You are an expert email prioritization AI.
Analyze this email and score its importance from 1-10.

Rules:
- 9-10: Urgent action needed (deadlines, emergencies, direct requests from important people)
- 7-8: Important, needs response soon (work emails, opportunities, interviews)
- 5-6: Good to know but not urgent (updates, newsletters from people you know)
- 3-4: Low priority (automated notifications, social updates)
- 1-2: Can ignore (promotional emails, spam, bulk newsletters)

Respond in JSON only, no extra text:
{
    "priority_score": 8,
    "priority_tag": "Action Required",
    "ai_explanation": "This email contains an urgent deadline."
}"""
        
        human_content = f"""
Email Details:
Subject: {item.get('title', 'No Subject')}
From: {item.get('author', 'Unknown')}
Body preview: {item.get('content', '')[:300]}
"""
        prompts.append([
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_content)
        ])
    
    try:
        # Run all prompts in parallel
        print(f"Prioritizing {len(items)} items individually via LLM batch...")
        responses = llm.batch(prompts)
        
        import re
        
        for idx, response in enumerate(responses):
            item = items[idx].copy()
            resp_text = response.content.strip()
            
            # Extract JSON block
            match = re.search(r'\{.*\}', resp_text, re.DOTALL)
            if match:
                try:
                    res = json.loads(match.group(0))
                    print(f"Gemini raw response: {resp_text}")
                    print(f"Parsed score: {res.get('priority_score')}")
                    
                    item["priority_score"] = int(res.get("priority_score", 0))
                    item["priority_tag"] = res.get("priority_tag", "FYI")
                    item["ai_explanation"] = res.get("ai_explanation", "Analyzed by AI")
                except Exception as parse_e:
                    print(f"JSON Parse Error for item {idx}: {parse_e}")
                    item["priority_score"] = 0
                    item["priority_tag"] = "Can Ignore"
                    item["ai_explanation"] = "Failed to parse AI response"
            else:
                print(f"No JSON found for item {idx}. Raw: {resp_text}")
                item["priority_score"] = 0
                item["priority_tag"] = "Can Ignore"
                item["ai_explanation"] = "No JSON found in AI response"
                
            prioritized.append(item)
            
    except Exception as e:
        import traceback
        print(f"Error in batch prioritization: {str(e)}")
        print(traceback.format_exc())
        # Fallback
        prioritized = items
        
    return {"prioritized_items": prioritized}
