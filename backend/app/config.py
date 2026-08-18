"""
Centralized configuration.

Every environment variable the app needs is read exactly once, here.
No other module should call os.environ / os.getenv directly - this
keeps credential handling auditable in one place and satisfies the
"store URI/username/password in environment variables" requirement.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # CognoDB connection (Bolt protocol, official Neo4j driver)
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str
    neo4j_database: str = "neo4j"

    # CORS
    allowed_origins: str = "http://localhost:5173"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """
    Cached so the .env file is parsed once per process, and every
    module that needs config gets the same Settings instance.
    """
    return Settings()
