"""Process liveness and dependency readiness endpoints."""

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from scenicops import __version__
from scenicops.api.schemas.health import HealthResponse, ReadinessResponse
from scenicops.core.config import get_settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live", response_model=HealthResponse)
def liveness() -> HealthResponse:
    """Report process liveness without checking external dependencies."""
    settings = get_settings()
    return HealthResponse(status="ok", service=settings.app_name, version=__version__)


@router.get("/ready", response_model=ReadinessResponse)
def readiness(request: Request) -> ReadinessResponse | JSONResponse:
    """Report whether the process is able to serve application traffic."""
    is_ready = bool(getattr(request.app.state, "is_ready", False))
    payload = ReadinessResponse(
        status="ready" if is_ready else "not_ready",
        checks={"application": "ok" if is_ready else "not_ready"},
    )
    if is_ready:
        return payload
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=payload.model_dump(mode="json"),
    )
