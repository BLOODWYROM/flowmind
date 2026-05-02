from dotenv import load_dotenv
load_dotenv('backend/.env')

from backend.agents.prioritizer import prioritize_data
from backend.agents.schema import AgentState

state = AgentState(
    user_id="test",
    fetched_items=[
        {
            "external_id": "1",
            "tool_name": "gmail",
            "title": "URGENT: Production is down",
            "content": "The database just crashed. Need immediate assistance.",
            "author": "boss@company.com"
        }
    ]
)

result = prioritize_data(state)
print("FINAL RESULT:")
import json
print(json.dumps(result, indent=2))
