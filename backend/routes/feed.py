from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc

from ..database import get_db
from ..models import Item, Summary
from ..agents.graph import run_pipeline

router = APIRouter()

@router.get("/items/{user_id}")
async def get_items(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Item)
        .where(Item.user_id == user_id)
        .order_by(desc(Item.priority_score))
    )
    items = result.scalars().all()
    return items

@router.get("/briefing/{user_id}")
async def get_briefing(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Summary)
        .where(Summary.user_id == user_id)
        .order_by(desc(Summary.date))
        .limit(1)
    )
    summary = result.scalars().first()
    return {"content": summary.content if summary else "No briefing generated yet. Run the pipeline to get started."}

@router.post("/trigger-pipeline/{user_id}")
async def trigger_pipeline(user_id: int, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    # Run the langgraph pipeline in the background
    background_tasks.add_task(run_pipeline, user_id)
    return {"status": "Pipeline triggered successfully in background."}
