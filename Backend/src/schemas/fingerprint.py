from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base
class FingerprintBase(BaseModel):
    name: str

# Requests
class FingerprintCreate(FingerprintBase):
    template_id: str

class FingerprintUpdate(BaseModel):
    name: Optional[str] = None
    enabled: Optional[bool] = None

# Responses
class FingerprintResponse(FingerprintBase):
    id: int
    enabled: bool
    created_at: datetime

    model_config = {"from_attributes": True}