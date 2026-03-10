from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Security
    secret_key: str
    device_api_key: str
    algorithm: str = "HS256"
    access_token_expire_hours: int = 24

    # Database
    database_url: str

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()