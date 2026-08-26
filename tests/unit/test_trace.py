"""Trace identifier safety tests."""

from scenicops.core.trace import resolve_trace_id


def test_resolve_trace_id_accepts_safe_value() -> None:
    assert resolve_trace_id("vehicle-42.event_7", fallback="fallback") == "vehicle-42.event_7"


def test_resolve_trace_id_rejects_oversized_value() -> None:
    assert resolve_trace_id("x" * 65, fallback="fallback") == "fallback"
