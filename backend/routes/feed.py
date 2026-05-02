from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
import logging
import traceback
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc

from ..database import get_db
from ..models import Item, Summary
from ..agents.graph import run_pipeline

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/items/{user_id}")
async def get_items(user_id: str, db: AsyncSession = Depends(get_db)):
    logger.info(f"Fetching items for user: {user_id}")
    try:
        result = await db.execute(
            select(Item)
            .where(Item.user_id == user_id)
            .order_by(desc(Item.priority_score))
        )
        items = result.scalars().all()
        logger.info(f"Found {len(items)} items for user {user_id}")
        return items
    except Exception as e:
        logger.error(f"Error fetching items for {user_id}: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/briefing/{user_id}")
async def get_briefing(user_id: str, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Summary)
            .where(Summary.user_id == user_id)
            .order_by(desc(Summary.date))
            .limit(1)
        )
        summary = result.scalars().first()
        return {"content": summary.content if summary else "No briefing generated yet. Run the pipeline to get started."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/trigger-pipeline/{user_id}")
async def trigger_pipeline(user_id: str, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    try:
        # Run the langgraph pipeline in the background
        background_tasks.add_task(run_pipeline, user_id)
        return {"status": "Pipeline triggered successfully in background."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
