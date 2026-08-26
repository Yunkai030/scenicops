"""Configuration validation tests."""

import pytest
from pydantic import ValidationError

from scenicops.core.config import Settings


def test_settings_reject_unknown_environment() -> None:
    with pytest.raises(ValidationError):
        Settings(environment="demo")  # type: ignore[arg-type]


def test_settings_reject_api_prefix_without_leading_slash() -> None:
    with pytest.raises(ValidationError):
        Settings(api_prefix="api/v1")
