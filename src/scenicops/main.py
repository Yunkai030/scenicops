"""FastAPI application factory and process entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import RequestResponseEndpoint

from scenicops import __version__
from scenicops.api.router import api_router
from scenicops.core.config import get_settings
from scenicops.core.logging import configure_logging, get_logger
from scenicops.core.trace import bind_trace_id, reset_trace_id, resolve_trace_id

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Own process-level resources and readiness state."""
    app.state.is_ready = True
    logger.info("application_started", extra={"app_version": __version__})
    try:
        yield
    finally:
        app.state.is_ready = False
        logger.info("application_stopped")


def create_app() -> FastAPI:
    """Create an isolated application instance for runtime and tests."""
    settings = get_settings()
    configure_logging(settings.log_level)

    application = FastAPI(
        title=settings.app_name,
        version=__version__,
        debug=settings.debug,
        lifespan=lifespan,
    )

    @application.middleware("http")
    async def request_context(
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        trace_id = resolve_trace_id(request.headers.get("X-Trace-ID"), fallback=uuid4().hex)
        token = bind_trace_id(trace_id)
        started_at = perf_counter()
        try:
            response = await call_next(request)
            response.headers["X-Trace-ID"] = trace_id
            logger.info(
                "request_completed",
                extra={
                    "http_method": request.method,
                    "http_path": request.url.path,
                    "http_status": response.status_code,
                    "duration_ms": round((perf_counter() - started_at) * 1000, 2),
                },
            )
            return response
        finally:
            reset_trace_id(token)

    application.include_router(api_router)
    return application


app = create_app()
