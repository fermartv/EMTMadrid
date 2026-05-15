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

    @pytest.mark.asyncio
    async def test_get_arrivals_with_bus_arrivals(self) -> None:
        """Test getting arrivals returns stop with bus arrivals."""
        stop_id = 123
        bus_arrivals = [
            TestData().a_bus_arrival(
                line="1",
                bus_id=100,
                destination="Destination A",
                estimate_arrive_sec=60,
            ),
            TestData().a_bus_arrival(
                line="2",
                bus_id=200,
                destination="Destination B",
                estimate_arrive_sec=120,
            ),
        ]
        expected_stop = TestData().a_stop(
            stop_id=stop_id,
            line_numbers=["1", "2"],
            bus_arrivals=bus_arrivals,
        )

        emt_repository = FakeEMTRepository()
        emt_repository.get_arrivals = AsyncMock(return_value=expected_stop)  # type: ignore[method-assign]

        get_arrivals = GetArrivals(emt_repository, stop_id)  # type: ignore
        stop = await get_arrivals.execute()

        assert stop.bus_arrivals == bus_arrivals
        assert len(stop.bus_arrivals) == 2
        assert stop.bus_arrivals[0].estimate_arrive_sec == 60
        assert stop.bus_arrivals[1].estimate_arrive_sec == 120
