import os
from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import field_validator

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from datetime import timezone, timedelta
    class ZoneInfo:
        def __init__(self, key):
            self.key = key

class Settings(BaseSettings):
    newsdata_api_key: str = ""
    currents_api_key: str = ""
    gnews_api_key: str = ""
    gemini_api_key: str = ""
    groq_api_key: str = ""
    database_url: str = "sqlite+aiosqlite:///./newspaper.db"
    newspaper_generation_time: str = "08:00"
    timezone: str = "Asia/Kolkata"
    max_generation_retries: int = 3
    environment: str = "development"
    secret_key: str = "digital_newspaper_secret_key_super_secure_2026_x99"
    log_level: str = "INFO"
    frontend_url: str = "http://localhost:3000"
    cors_origins: Union[List[str], str] = ["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000"]
    sentry_dsn: str = ""
    gemini_daily_limit: int = 1000
    groq_daily_token_limit: int = 200000

    @field_validator("cors_origins", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["*"]

    @property
    def tz(self):
        try:
            return ZoneInfo(self.timezone)
        except Exception:
            from datetime import timezone, timedelta
            return timezone(timedelta(hours=5, minutes=30))

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    model_config = {
        "env_file": os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        "case_sensitive": False,
        "extra": "ignore"
    }

settings = Settings()
