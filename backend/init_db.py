import asyncio
from database import engine, Base, AsyncSessionLocal
from models import User

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with AsyncSessionLocal() as session:
        user = User(id=1, email="dev@example.com", name="Developer")
        session.add(user)
        try:
            await session.commit()
            print("Mock user created.")
        except Exception as e:
            print("User might already exist or error:", e)

if __name__ == "__main__":
    asyncio.run(init_db())
