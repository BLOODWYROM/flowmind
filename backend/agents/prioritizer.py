from .schema import AgentState
from groq import Groq
import json
import os
import re
import traceback

MODEL = "llama-3.1-8b-instant"

def prioritize_data(state: AgentState):
    """
    Uses Groq API to score and tag fetched items
    in a single bulk API call to avoid rate limits.
    """
    _api_key = os.environ.get("GROQ_API_KEY", "")
    if not _api_key:
        print("WARNING: GROQ_API_KEY is not set.")
    
    try:
        client = Groq(api_key=_api_key)
    except Exception as e:
        print(f"Failed to initialize Groq Client: {e}")
        return {"prioritized_items": state.fetched_items}
    
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

    # Build the payload, capping at 30 items to avoid Groq Free Tier TPM limits
    payload = []
    for item in items[:30]:
        payload.append({
            "external_id": item["external_id"],
            "tool": item.get("tool_name", "unknown"),
            "subject": item.get("title", "No Subject"),
            "sender": item.get("author", "Unknown"),
            "body_preview": item.get("content", "")[:100]  # Reduced from 300 to 100
        })

    human_content = json.dumps(payload, indent=2)

    try:
        print(f"GROQ KEY EXISTS: {bool(_api_key)}")
        print(f"Prioritizing {len(items)} items using Groq SDK (model: {MODEL})...")

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Items to analyze:\n{human_content}"}
            ]
        )
        resp_text = response.choices[0].message.content.strip()

        # Strip markdown fences if present
        resp_text = resp_text.replace("```json", "").replace("```", "").strip()

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
                        item["priority_score"] = 3
                        item["priority_tag"] = "Low Priority"
                        item["ai_explanation"] = "Not individually scored in this batch."

                    prioritized.append(item)

            except Exception as parse_e:
                print(f"JSON Parse Error: {parse_e}")
                print(f"Raw Response was: {resp_text[:500]}")
                prioritized = items
        else:
            print(f"No JSON block found in response. Raw: {resp_text[:500]}")
            prioritized = items

    except Exception as e:
        print(f"Error in prioritization: {str(e)}")
        print(traceback.format_exc())
        prioritized = items

    return {"prioritized_items": prioritized}
