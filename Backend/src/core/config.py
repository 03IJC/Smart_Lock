from pydantic_settings import BaseSettings, SettingsConfigDict


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

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()