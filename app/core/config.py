from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings and environment variables.
    Values are overridden by environment variables or a .env file.
    """
    app_name: str = "Address Book API"
    debug: bool = False
    database_url: str = "sqlite:///./address_book.db"
    api_v1_prefix: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()
