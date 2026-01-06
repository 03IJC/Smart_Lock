from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base
class UserBase(BaseModel):
    name: str
    username: str

# Requests
class UserCreate(UserBase):
    password: str
    role: str = "admin"

class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None

# Responses
class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}