"""Health endpoint contract tests."""

from typing import Any

from fastapi.testclient import TestClient

from scenicops.main import create_app


def test_liveness_contract(client: TestClient) -> None:
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "ScenicOps API",
        "version": "0.1.0",
    }
    assert response.headers["X-Trace-ID"]


def test_readiness_reports_application_state(client: TestClient) -> None:
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "checks": {"application": "ok"},
    }


def test_readiness_returns_503_when_application_is_not_ready() -> None:
    application = create_app()
    with TestClient(application) as client:
        application.state.is_ready = False
        response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {
        "status": "not_ready",
        "checks": {"application": "not_ready"},
    }


def test_valid_trace_id_is_preserved(client: TestClient) -> None:
    response = client.get("/health/live", headers={"X-Trace-ID": "demo-trace_001"})

    assert response.headers["X-Trace-ID"] == "demo-trace_001"


def test_unsafe_trace_id_is_replaced(client: TestClient) -> None:
    response = client.get("/health/live", headers={"X-Trace-ID": "bad trace\nvalue"})

    trace_id = response.headers["X-Trace-ID"]
    assert trace_id != "bad trace\nvalue"
    assert len(trace_id) == 32


def test_openapi_exposes_typed_health_contracts(client: TestClient) -> None:
    document: dict[str, Any] = client.get("/openapi.json").json()

    assert "/health/live" in document["paths"]
    assert "/health/ready" in document["paths"]
    assert "HealthResponse" in document["components"]["schemas"]
    assert "ReadinessResponse" in document["components"]["schemas"]
