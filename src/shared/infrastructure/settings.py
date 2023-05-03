from pydantic import BaseSettings
from typing import Callable


class Settings(BaseSettings):
    # APP
    API_VERSION: str = "v1"
    NAMESPACE: str = "users"
    # MONGO
    MONGO_URI: str
    MONGO_DB_NAME: str
    MONGO_TIMEOUT_MS: int = 500
    MONGO_MAX_POOL_SIZE: int = 20


def _configure_initial_settings() -> Callable[[], Settings]:
    settings = Settings()

    def load() -> Settings:
        return settings

    return load


get_settings = _configure_initial_settings()
