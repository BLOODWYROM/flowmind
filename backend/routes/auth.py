from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from ..database import get_db
from ..models import User, Integration

router = APIRouter()

class SyncUserRequest(BaseModel):
    id: str
    email: str
    name: str

@router.post("/sync-user")
async def sync_user(req: SyncUserRequest, db: AsyncSession = Depends(get_db)):
    # Since NextAuth provides string IDs, we will store it, but wait, our User model has Integer ID!
    # Let's map the email to a user. If the email doesn't exist, create it.
    result = await db.execute(select(User).where(User.email == req.email))
    user = result.scalars().first()
    
    if not user:
        user = User(email=req.email, name=req.name)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
    return {"user_id": user.id, "email": user.email, "name": user.name}

class ConnectToolRequest(BaseModel):
    user_id: int
    tool_name: str # github, gmail

@router.post("/connect-tool")
async def connect_tool(req: ConnectToolRequest, db: AsyncSession = Depends(get_db)):
    # Mocking the OAuth connection by just saving a fake token
    result = await db.execute(
        select(Integration).where(
            Integration.user_id == req.user_id, 
            Integration.tool_name == req.tool_name
        )
    )
    integration = result.scalars().first()
    
    if not integration:
        integration = Integration(
            user_id=req.user_id,
            tool_name=req.tool_name,
            access_token=f"mock_{req.tool_name}_token"
        )
        db.add(integration)
    else:
        integration.is_active = True
        
    await db.commit()
    return {"status": "success", "tool": req.tool_name}

@router.get("/status/{user_id}")
async def integration_status(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Integration).where(Integration.user_id == user_id))
    integrations = result.scalars().all()
    
    return {
        "github": any(i.tool_name == "github" and i.is_active for i in integrations),
        "gmail": any(i.tool_name == "gmail" and i.is_active for i in integrations)
    }
