from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
import logging
import traceback
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from ..database import get_db
from ..models import User, Integration

router = APIRouter()
logger = logging.getLogger(__name__)

class SyncUserRequest(BaseModel):
    id: str
    email: str
    name: str
    image_url: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    provider: Optional[str] = "github"

@router.post("/sync-user")
async def sync_user(req: SyncUserRequest, db: AsyncSession = Depends(get_db)):
    logger.info(f"Syncing user: {req.email} with ID: {req.id}")
    try:
        # Use req.id (the Google/GitHub ID string) as the primary key
        # Check if user already exists by EMAIL for account linking
        result = await db.execute(select(User).where(User.email == req.email))
        user = result.scalars().first()
        
        if not user:
            # First time logging in with this email
            user = User(id=req.id, email=req.email, name=req.name, image_url=req.image_url)
            db.add(user)
        else:
            # Existing user found by email, update details
            user.name = req.name
            user.image_url = req.image_url
            # We keep the original user.id to preserve database relationships
            
        await db.commit()
        await db.refresh(user)
        
        if req.access_token and req.provider:
            # Check if integration already exists for this provider
            int_result = await db.execute(
                select(Integration).where(
                    Integration.user_id == user.id, 
                    Integration.tool_name == req.provider
                )
            )
            integration = int_result.scalars().first()
            
            if integration:
                integration.access_token = req.access_token
                if req.refresh_token:
                    integration.refresh_token = req.refresh_token
                integration.is_active = True
            else:
                new_integration = Integration(
                    user_id=user.id,
                    tool_name=req.provider,
                    access_token=req.access_token,
                    refresh_token=req.refresh_token,
                    is_active=True
                )
                db.add(new_integration)
            
            await db.commit()
            
        return {"user_id": user.id, "email": user.email, "name": user.name}
    except Exception as e:
        print(f"Error in sync_user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class ConnectToolRequest(BaseModel):
    user_id: str
    tool_name: str # github, gmail

@router.post("/connect-tool")
async def connect_tool(req: ConnectToolRequest, db: AsyncSession = Depends(get_db)):
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{user_id}")
async def integration_status(user_id: str, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Integration).where(Integration.user_id == user_id))
        integrations = result.scalars().all()
        
        return {
            "github": any(i.tool_name == "github" and i.is_active for i in integrations),
            "gmail": any(i.tool_name in ["google", "gmail"] and i.is_active for i in integrations),
            "slack": any(i.tool_name == "slack" and i.is_active for i in integrations)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
