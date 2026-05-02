from pydantic import BaseModel, Field
from typing import List, Optional

class AgentState(BaseModel):
    user_id: str
    fetched_items: List[dict] = Field(default_factory=list)
    prioritized_items: List[dict] = Field(default_factory=list)
    summary: Optional[str] = None
