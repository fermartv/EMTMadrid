"""Unit tests for the main module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiohttp import ClientSession

from emt_madrid.main import EMTClient
from emt_madrid.use_cases.get_arrivals import GetArrivals
from emt_madrid.use_cases.get_stop_info import GetStopInfo
from tests.unit.test_data import TestData


class TestEMTClient:
    """Test cases for the EMTClient class."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock aiohttp ClientSession."""
        return MagicMock(spec=ClientSession)

    @pytest.fixture
    def emt_client(self, mock_session):
        """Create an EMTClient instance for testing."""
        return EMTClient(
            email="test@example.com",
            password="testpass",
            stop_id=123,
            session=mock_session,
            lines=["1", "2"],
        )

    @pytest.mark.asyncio
    async def test_get_stop_info(self, emt_client):
        """Test getting stop information."""
        mock_use_case = AsyncMock(spec=GetStopInfo)
        mock_use_case.execute.return_value = TestData().a_stop()

        with patch(
            "emt_madrid.main.GetStopInfo", return_value=mock_use_case
        ) as mock_constructor:
            result = await emt_client.get_stop_info()

            mock_constructor.assert_called_once_with(
                emt_client._repository, emt_client._stop_id, emt_client._lines
            )
            mock_use_case.execute.assert_awaited_once()
            assert emt_client._stop == TestData().a_stop()
            assert result == TestData().a_stop()

    @pytest.mark.asyncio
    async def test_get_arrivals_without_previous_stop(self, emt_client):
        """Test getting arrivals when no stop info has been fetched yet."""
        emt_client.get_stop_info = AsyncMock(return_value=TestData().a_stop())

        mock_use_case = AsyncMock(spec=GetArrivals)
        mock_use_case.execute.return_value = TestData().a_stop()

        with patch("emt_madrid.main.GetArrivals", return_value=mock_use_case):
            result = await emt_client.get_arrivals()

            emt_client.get_stop_info.assert_awaited_once()
            assert result == TestData().a_stop()

    @pytest.mark.asyncio
    async def test_get_arrivals_with_existing_stop(self, emt_client):
        """Test getting arrivals when stop info is already available."""
        emt_client._stop = TestData().a_stop()

        mock_use_case = AsyncMock(spec=GetArrivals)
        mock_use_case.execute.return_value = TestData().a_stop()

        with patch("emt_madrid.main.GetArrivals", return_value=mock_use_case):
            result = await emt_client.get_arrivals()

            assert not hasattr(emt_client.get_stop_info, "assert_awaited")
            assert result == TestData().a_stop()
