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

        # 2. Fetch Gmail Integration
        result = await db.execute(
            select(Integration).where(
                Integration.user_id == user_id,
                Integration.tool_name == "google",
                Integration.is_active == True
            )
        )
        gmail_int = result.scalars().first()
        
        print(f"[GMAIL DEBUG] User {user_id}: gmail_int found = {gmail_int is not None}")
        if gmail_int:
            print(f"[GMAIL DEBUG] Token exists = {bool(gmail_int.access_token)}, token length = {len(gmail_int.access_token) if gmail_int.access_token else 0}")
        
        if gmail_int and gmail_int.access_token:
            try:
                headers = {"Authorization": f"Bearer {gmail_int.access_token}"}
                async with httpx.AsyncClient() as client:
                    # Fetch ALL recent messages (not just unread)
                    resp = await client.get("https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=15", headers=headers)
                    print(f"[GMAIL DEBUG] Messages list response: status={resp.status_code}")
                    if resp.status_code != 200:
                        print(f"[GMAIL DEBUG] Error response body: {resp.text}")
                    if resp.status_code == 200:
                        messages = resp.json().get("messages", [])
                        print(f"[GMAIL DEBUG] Found {len(messages)} messages")
                        for msg in messages:
                            # Fetch message details
                            m_resp = await client.get(f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg['id']}", headers=headers)
                            if m_resp.status_code == 200:
                                m_data = m_resp.json()
                                headers_list = m_data["payload"]["headers"]
                                subject = next((h["value"] for h in headers_list if h["name"] == "Subject"), "No Subject")
                                sender = next((h["value"] for h in headers_list if h["name"] == "From"), "Unknown")
                                items.append({
                                    "tool_name": "gmail",
                                    "external_id": msg["id"],
                                    "title": subject,
                                    "content": m_data["snippet"],
                                    "url": f"https://mail.google.com/mail/u/0/#all/{m_data['threadId']}",
                                    "author": sender,
                                    "timestamp": datetime.datetime.fromtimestamp(int(m_data["internalDate"])/1000).isoformat()
                                })
            except Exception as e:
                print(f"[GMAIL DEBUG] Exception fetching Gmail data: {e}")
        else:
            print(f"[GMAIL DEBUG] No active Google integration found for user {user_id}")

    # Fallback/Empty message if no data found
    if not items:
        now = datetime.datetime.utcnow()
        items = [
            {
                "tool_name": "github",
                "external_id": "welcome_1",
                "title": "Welcome to FlowMind!",
                "content": "Connect your GitHub or Google account to see real AI-prioritized notifications here.",
                "url": "https://github.com",
                "author": "FlowMind AI",
                "timestamp": now.isoformat()
            }
        ]
        
    return {"fetched_items": items}
