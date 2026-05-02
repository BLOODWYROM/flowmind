from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

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
    allow_origins=[
        "https://flowmind-phi.vercel.app",
        "https://flowmind-49n9cn8hy-bloodwyroms-projects.vercel.app",
        "http://localhost:3000",
    ],
    allow_credentials=True,
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
