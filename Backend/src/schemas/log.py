from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict, Optional

from ..models.log import EventType

# Requests
class LogFilter(BaseModel):
    event_type: Optional[EventType] = None
    lock_id: Optional[int] = None
    user_id: Optional[int] = None
    success: Optional[bool] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

# Responses
class LogResponse(BaseModel):
    id: int
    event_type: EventType

    lock_id: Optional[int]
    fingerprint_id: Optional[int]
    user_id: Optional[int]

    success: bool
    timestamp: datetime
    event_metadata: Optional[Dict[str, Any]]

    model_config = {"from_attributes": True}

class PaginatedLogs(BaseModel):
    items: list[LogResponse]
    total: int
    limit: int
    offset: int