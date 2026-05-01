from .schema import AgentState
import datetime

import httpx
import datetime
from ..database import AsyncSessionLocal
from ..models import Integration
from sqlalchemy import select

async def fetch_data(state: AgentState):
    """
    Fetches real data from GitHub if a token is available.
    """
    user_id = state["user_id"]
    items = []
    
    async with AsyncSessionLocal() as db:
        # 1. Fetch GitHub Integration
        result = await db.execute(
            select(Integration).where(
                Integration.user_id == user_id,
                Integration.tool_name == "github",
                Integration.is_active == True
            )
        )
        github_int = result.scalars().first()
        
        if github_int and github_int.access_token:
            try:
                headers = {
                    "Authorization": f"Bearer {github_int.access_token}",
                    "Accept": "application/vnd.github.v3+json"
                }
                # Fetch recent notifications or issues
                async with httpx.AsyncClient() as client:
                    resp = await client.get("https://api.github.com/notifications", headers=headers)
                    if resp.status_code == 200:
                        notifications = resp.json()
                        for note in notifications[:10]:
                            items.append({
                                "tool_name": "github",
                                "external_id": note["id"],
                                "title": note["subject"]["title"],
                                "content": f"New notification: {note['reason']}",
                                "url": note["subject"]["url"].replace("api.github.com/repos", "github.com"), # Simple conversion
                                "author": note["repository"]["full_name"],
                                "timestamp": note["updated_at"]
                            })
            except Exception as e:
                print(f"Error fetching GitHub data: {e}")

    # Fallback/Mock data for Gmail (since we don't have Gmail OAuth set up yet)
    if not items:
        now = datetime.datetime.utcnow()
        items = [
            {
                "tool_name": "github",
                "external_id": "mock_pr_1",
                "title": "Welcome to FlowMind!",
                "content": "You haven't connected your GitHub account yet, or there are no new notifications. Connect in the sidebar to see real data!",
                "url": "https://github.com",
                "author": "FlowMind-AI",
                "timestamp": now.isoformat()
            }
        ]
        
    return {"fetched_items": items}
