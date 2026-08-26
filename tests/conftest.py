"""Shared test fixtures."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from scenicops.main import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Run every API test with lifespan startup and shutdown."""
    with TestClient(create_app()) as test_client:
        yield test_client
