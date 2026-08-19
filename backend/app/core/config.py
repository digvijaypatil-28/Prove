import os
from pydantic_settings import BaseSettings

from pydantic import ConfigDict

class Settings(BaseSettings):
    LLM_PROVIDER: str = "mock"
    GEMINI_API_KEY: str = ""
    DATABASE_URL: str = "sqlite:///./prove.db"
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    model_config = ConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
