from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from contextlib import asynccontextmanager
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


from .database import engine, Base, get_db
from .routes import auth, feed

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="FlowMind MVP", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(feed.router, prefix="/api/feed", tags=["feed"])

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.get("/api/reset-db")
async def reset_db():
    """Nuclear option: Drops all tables and recreates them with the new schema."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        return {"status": "success", "message": "Database completely wiped and recreated with the latest schema."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
@app.get("/api/debug/db-peek")
async def db_peek(db: AsyncSession = Depends(get_db)):
    """Debug endpoint to see if data is actually in the DB."""
    from sqlalchemy import func
    from .models import Item, User, Integration
    
    # Count items per user
    item_result = await db.execute(select(Item.user_id, func.count(Item.id)).group_by(Item.user_id))
    item_counts = {row[0]: row[1] for row in item_result.all()}
    
    # List users and their integrations
    user_result = await db.execute(select(User))
    users = user_result.scalars().all()
    
    debug_data = []
    for u in users:
        int_result = await db.execute(select(Integration).where(Integration.user_id == u.id))
        integrations = int_result.scalars().all()
        
        # Get actual items to see their scores
        item_raw = await db.execute(select(Item).where(Item.user_id == u.id).limit(5))
        db_items = item_raw.scalars().all()
        
        tools = []
        for i in integrations:
            tools.append({
                "name": i.tool_name,
                "has_token": bool(i.access_token),
                "token_preview": i.access_token[:10] + "..." if i.access_token else "NONE",
                "has_refresh": bool(i.refresh_token)
            })
            
        debug_data.append({
            "user_id": u.id,
            "email": u.email,
            "item_count": item_counts.get(u.id, 0),
            "integrations": tools,
            "item_samples": [
                {
                    "title": it.title[:30] if it.title else "No Title",
                    "score": it.priority_score,
                    "tag": it.priority_tag
                } for it in db_items
            ]
        })
        
    return debug_data
