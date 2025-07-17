import pytest

from emt_madrid.infrastructure.http_client import HTTPClient


class FakeConfig:
    """Fake configuration for testing HTTP client."""

    BASE_URL = "https://http.codes/"


class TestHTTPClient:
    """Test cases for HTTPClient class."""

    @pytest.mark.asyncio
    async def test_config(self) -> None:
        """Test HTTP client initialization with config."""
        http_client = HTTPClient(config=FakeConfig())  # type: ignore
        assert http_client.base_url == FakeConfig.BASE_URL
