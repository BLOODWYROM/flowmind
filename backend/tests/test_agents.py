from backend.agents.schema import AgentState
from backend.agents.fetcher import fetch_data

def test_fetcher():
    """Test that the mock fetcher returns a valid list of items."""
    state = AgentState(user_id=1)
    result = fetch_data(state)
    
    assert "fetched_items" in result
    assert isinstance(result["fetched_items"], list)
    assert len(result["fetched_items"]) > 0
    
    first_item = result["fetched_items"][0]
    assert "tool_name" in first_item
    assert "title" in first_item
    assert "content" in first_item

# Note: In a real test suite, you would mock the LLM calls for the prioritizer and summarizer.
# For example, using pytest-mock to mock ChatGoogleGenerativeAI.invoke.
