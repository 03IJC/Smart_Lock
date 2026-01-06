from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from ..models.lock import LockStatus

# Base
class LockBase(BaseModel):
    name: str

# Requests
class LockCreate(LockBase):
    pass

class LockUpdate(BaseModel):
    name: Optional[str] = None

# Responses
class LockResponse(LockBase):
    id: int
    status: LockStatus
    last_heartbeat: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}