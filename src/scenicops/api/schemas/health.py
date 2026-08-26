"""Health endpoint response contracts."""

from typing import Literal

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """Liveness response that is stable for monitoring clients."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok"]
    service: str
    version: str
    environment: str


class ReadinessResponse(BaseModel):
    """Readiness response with explicit component checks."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ready", "not_ready"]
    checks: dict[str, Literal["ok", "not_ready"]]
