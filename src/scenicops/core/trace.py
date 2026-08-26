"""Trace identifier validation and context propagation."""

import re
from contextvars import ContextVar, Token

_TRACE_ID_PATTERN = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
_trace_id: ContextVar[str] = ContextVar("trace_id", default="-")


def resolve_trace_id(candidate: str | None, *, fallback: str) -> str:
    """Accept a bounded safe identifier or replace it with a generated value."""
    if candidate and _TRACE_ID_PATTERN.fullmatch(candidate):
        return candidate
    return fallback


def bind_trace_id(trace_id: str) -> Token[str]:
    """Bind a trace identifier to the current async context."""
    return _trace_id.set(trace_id)


def reset_trace_id(token: Token[str]) -> None:
    """Restore the prior async context after request completion."""
    _trace_id.reset(token)


def current_trace_id() -> str:
    """Read the trace identifier for logs and downstream calls."""
    return _trace_id.get()
