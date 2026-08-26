"""Environment-backed application settings."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated runtime configuration loaded from SCENICOPS_* variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="SCENICOPS_",
        extra="ignore",
    )

    app_name: str = "ScenicOps API"
    environment: Literal["local", "test", "staging", "production"] = "local"
    debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    api_prefix: str = Field(default="/api/v1", pattern=r"^/[a-z0-9/_-]+$")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return one immutable configuration snapshot per process."""
    return Settings()
