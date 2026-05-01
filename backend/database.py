import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Load .env file
load_dotenv()

# Use DATABASE_URL from environment if it exists (e.g., Neon Postgres), otherwise fallback to local SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./flowmind.db")

# If user provided a postgres:// url from Neon, we must use the asyncpg driver
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# asyncpg doesn't support 'sslmode' in the connection string and throws a TypeError.
# We strip the query parameters (like ?sslmode=require) since asyncpg handles SSL automatically.
if "postgresql+asyncpg" in DATABASE_URL and "?" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0]

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
