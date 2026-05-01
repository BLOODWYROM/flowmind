from langgraph.graph import StateGraph, END
from .schema import AgentState
from .fetcher import fetch_data
from .prioritizer import prioritize_data
from .summarizer import summarize_data
import asyncio
import datetime

# We need a way to run database operations async in the graph, or wrap it.
from ..database import AsyncSessionLocal
from ..models import Item, Summary

# Define the graph
workflow = StateGraph(AgentState)

workflow.add_node("fetch_data", fetch_data)
workflow.add_node("prioritize_data", prioritize_data)
workflow.add_node("summarize_data", summarize_data)

workflow.set_entry_point("fetch_data")
workflow.add_edge("fetch_data", "prioritize_data")
workflow.add_edge("prioritize_data", "summarize_data")
workflow.add_edge("summarize_data", END)

app_graph = workflow.compile()

async def run_pipeline(user_id: int):
    """
    Runs the langgraph pipeline and saves results to the database.
    """
    initial_state = AgentState(user_id=user_id)
    
    # Run the graph (invoke is sync, but nodes are just processing dictionaries)
    result = app_graph.invoke(initial_state)
    
    # Save to database
    async with AsyncSessionLocal() as session:
        # Save items
        for it in result["prioritized_items"]:
            # Check if exists
            new_item = Item(
                user_id=user_id,
                tool_name=it["tool_name"],
                external_id=it["external_id"],
                title=it["title"],
                content=it["content"],
                url=it["url"],
                author=it["author"],
                timestamp=datetime.datetime.fromisoformat(it["timestamp"]),
                priority_score=it.get("priority_score"),
                priority_tag=it.get("priority_tag"),
                ai_explanation=it.get("ai_explanation")
            )
            session.add(new_item)
            
        # Save summary
        if result["summary"]:
            new_summary = Summary(
                user_id=user_id,
                content=result["summary"]
            )
            session.add(new_summary)
            
        await session.commit()
    
    print(f"Pipeline completed for user {user_id}")
