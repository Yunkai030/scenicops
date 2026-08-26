"""Small JSON logging setup with trace correlation."""

import json
import logging
from datetime import UTC, datetime
from typing import Any

from scenicops.core.trace import current_trace_id


class JsonFormatter(logging.Formatter):
    """Serialize stable log fields as one JSON object per line."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "trace_id": current_trace_id(),
        }
        for key in ("app_version", "http_method", "http_path", "http_status", "duration_ms"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, default=str)


def configure_logging(level: str) -> None:
    """Configure root logging once for API and future worker processes."""
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if not any(getattr(handler, "_scenicops_handler", False) for handler in root_logger.handlers):
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        handler._scenicops_handler = True  # type: ignore[attr-defined]
        root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Return a standard library logger configured at app creation time."""
    return logging.getLogger(name)
