from pydantic import BaseModel
from ..models.lock import LockStatus

# Requests
class LockHeartbeat(BaseModel):
    status: LockStatus

class AccessAttempt(BaseModel):
    template_id: str
    lock_id: int

# Response
class AccessResponse(BaseModel):
    granted: bool