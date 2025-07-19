from unittest.mock import AsyncMock

import pytest

from emt_madrid.use_cases.get_arrivals import GetArrivals
from tests.unit.test_data import TestData
from tests.unit.use_cases.test_fixtures import FakeEMTRepository


class TestGetArrivals:
    """Test cases for GetArrivals use case."""

    @pytest.mark.asyncio
    async def test_get_arrivals(self) -> None:
        """Test getting arrivals for a stop."""
        stop_id = 123
        expected_stop = TestData().a_stop(stop_id=stop_id)

        emt_repository = FakeEMTRepository()
        mock_get_arrivals = AsyncMock(return_value=expected_stop)
        emt_repository.get_arrivals = mock_get_arrivals  # type: ignore[method-assign]

        get_arrivals = GetArrivals(emt_repository, stop_id)  # type: ignore
        stop = await get_arrivals.execute()

        assert stop.stop_lines == expected_stop.stop_lines
        mock_get_arrivals.assert_called_once_with(stop_id)

    @pytest.mark.asyncio
    async def test_get_arrivals_raises_error(self) -> None:
        """Test error handling when getting arrivals fails."""
        stop = TestData().a_stop(stop_id=123)
        error_message = f"No arrival information found for stop {stop.stop_id}"

        emt_repository = FakeEMTRepository()
        emt_repository.get_arrivals = AsyncMock(side_effect=ValueError(error_message))  # type: ignore[method-assign]

        get_arrivals = GetArrivals(emt_repository, stop)  # type: ignore

        with pytest.raises(ValueError, match=error_message):
            await get_arrivals.execute()
