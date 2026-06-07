from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    All config is loaded from environment variables or a .env file.
    Pydantic validates types automatically — e.g. DATABASE_URL must be a string.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # App
    app_name: str = "HMS"
    environment: str = "development"
    debug: bool = True

    # Database
    database_url: str = "postgresql+asyncpg://hms:hms@localhost:5432/hms"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Zalo OA — filled in when you register your Official Account
    zalo_oa_id: str = ""
    zalo_access_token: str = ""
    zalo_secret_key: str = ""

    # Future: OTA integrations
    # booking_com_api_key: str = ""
    # agoda_api_key: str = ""


# Single instance imported everywhere: from app.core.config import settings
settings = Settings()
