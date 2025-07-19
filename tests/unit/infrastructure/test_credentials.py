"""Tests for the Credentials class."""

from __future__ import annotations

import pytest

from emt_madrid.infrastructure.emt_api_client import (
    Credentials,
    InvalidCredentialsError,
)


def test_credentials_initialization() -> None:
    """Test Credentials initialization with valid values."""
    email = "test@example.com"
    password = "password123"
    credentials = Credentials(email=email, password=password)
    assert credentials.email == email
    assert credentials.password == password


def test_credentials_none_values() -> None:
    """Test Credentials initialization with None values raises error."""
    # Test None email
    with pytest.raises(InvalidCredentialsError):
        Credentials(email=None, password="password")  # type: ignore[arg-type]

    # Test None password
    with pytest.raises(InvalidCredentialsError):
        Credentials(email="email@example.com", password=None)  # type: ignore[arg-type]

    # Test both None
    with pytest.raises(InvalidCredentialsError):
        Credentials(email=None, password=None)  # type: ignore[arg-type]


def test_credentials_empty_strings() -> None:
    """Test that empty strings are not allowed."""
    with pytest.raises(InvalidCredentialsError):
        Credentials(email="", password="password")

    with pytest.raises(InvalidCredentialsError):
        Credentials(email="email@example.com", password="")

    with pytest.raises(InvalidCredentialsError):
        Credentials(email="", password="")
