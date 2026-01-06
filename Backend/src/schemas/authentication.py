from pydantic import BaseModel

# Requests
class LoginRequest(BaseModel):
    username: str
    password: str

# Responses
class TokenResponse(BaseModel):
    """
        JWT access token response.
    """
    access_token: str
    expires_at: int
    token_type: str = "bearer"

