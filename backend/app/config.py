from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    cache_ttl_seconds: int = 300
    cors_origins: str = "http://localhost:3000"
    linkedin_access_token: str | None = None
    linkedin_api_base_url: str = "https://api.linkedin.com"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
