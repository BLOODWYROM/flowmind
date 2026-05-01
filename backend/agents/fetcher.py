from .schema import AgentState
import datetime

def fetch_data(state: AgentState):
    """
    Mock data fetcher. In a real app, this would use the user's OAuth tokens
    from the database to hit GitHub/Gmail APIs.
    """
    # Mock some recent items
    now = datetime.datetime.utcnow()
    mock_items = [
        {
            "tool_name": "github",
            "external_id": "pr_123",
            "title": "Fix memory leak in DataFetcher",
            "content": "I noticed the DataFetcher doesn't close sessions properly. This PR adds a context manager to fix it. Please review ASAP as this is blocking deployment.",
            "url": "https://github.com/org/repo/pull/123",
            "author": "john_doe",
            "timestamp": (now - datetime.timedelta(minutes=30)).isoformat()
        },
        {
            "tool_name": "github",
            "external_id": "issue_456",
            "title": "Update README with setup instructions",
            "content": "We need to document the new env vars for OAuth.",
            "url": "https://github.com/org/repo/issues/456",
            "author": "jane_smith",
            "timestamp": (now - datetime.timedelta(hours=2)).isoformat()
        },
        {
            "tool_name": "gmail",
            "external_id": "email_789",
            "title": "URGENT: Production database high CPU usage",
            "content": "Alert: The main postgres database is consistently hitting 95% CPU. We might need to scale up the instance immediately.",
            "url": "https://mail.google.com/mail/u/0/#inbox/123",
            "author": "aws-alerts@company.com",
            "timestamp": (now - datetime.timedelta(minutes=5)).isoformat()
        },
        {
            "tool_name": "gmail",
            "external_id": "email_101",
            "title": "Weekly Engineering Newsletter",
            "content": "Here's what happened this week in the tech world...",
            "url": "https://mail.google.com/mail/u/0/#inbox/456",
            "author": "newsletter@techweekly.com",
            "timestamp": (now - datetime.timedelta(hours=5)).isoformat()
        }
    ]
    
    return {"fetched_items": mock_items}
