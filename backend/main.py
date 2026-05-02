from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Langchain expects GOOGLE_API_KEY
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

from .database import engine, Base
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
        int_result = await db.execute(select(Integration.tool_name).where(Integration.user_id == u.id))
        tools = [r[0] for r in int_result.all()]
        debug_data.append({
            "user_id": u.id,
            "email": u.email,
            "item_count": item_counts.get(u.id, 0),
            "integrations": tools
        })
        
    return debug_data
