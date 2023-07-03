from typing import List

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    class Config:
        case_sensitive = True


settings = Settings()
