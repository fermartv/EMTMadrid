from unittest.mock import AsyncMock

import pytest

from emt_madrid.domain.exceptions import APIResponseError
from emt_madrid.use_cases.get_stop_info import GetStopInfo
from tests.unit.test_data import TestData
from tests.unit.use_cases.test_fixtures import FakeEMTRepository


class TestGetStopInfo:
    """Test cases for GetStopInfo use case."""

    @pytest.mark.asyncio
    async def test_get_stop_info_without_lines_filter(self) -> None:
        """Test getting stop info without line filtering."""
        stop_id = 123
        expected_stop = TestData().a_stop(stop_id=stop_id, line_numbers=["1", "2", "3"])

        emt_repository = FakeEMTRepository()
        mock_get_stop_info = AsyncMock(return_value=expected_stop)
        emt_repository.get_stop_info = mock_get_stop_info  # type: ignore[method-assign]

        get_stop_info = GetStopInfo(emt_repository, stop_id)  # type: ignore
        stop = await get_stop_info.execute()

        assert stop.stop_lines == expected_stop.stop_lines
        mock_get_stop_info.assert_called_once_with(stop_id)

    @pytest.mark.asyncio
    async def test_get_stop_info_with_filtered_lines(self) -> None:
        """Test getting stop info with specific line filtering."""
        stop_id = 123
        lines = ["1", "2"]

        expected_stop = TestData().a_stop(stop_id=stop_id, line_numbers=lines)

        emt_repository = FakeEMTRepository()
        emt_repository.get_stop_info = AsyncMock(return_value=expected_stop)  # type: ignore[method-assign]

        get_stop_info = GetStopInfo(emt_repository, stop_id, lines)  # type: ignore
        stop = await get_stop_info.execute()

        assert stop.stop_id == stop_id
        assert stop.stop_name == "Test Stop"
        assert stop.stop_address == "Test Address"
        assert stop.stop_coordinates == [0, 0]
        assert stop.stop_lines == expected_stop.stop_lines

    @pytest.mark.asyncio
    async def test_raise_error_when_lines_not_available_at_stop(self) -> None:
        stop_id = 123
        found_lines = ["1", "2"]
        missing_lines = ["3", "4"]
        expected_lines = found_lines + missing_lines
        expected_error_message = (
            f"The following lines are not available at this stop: {missing_lines}"
        )

        expected_stop = TestData().a_stop(stop_id=stop_id, line_numbers=found_lines)

        emt_repository = FakeEMTRepository()
        emt_repository.get_stop_info = AsyncMock(return_value=expected_stop)  # type: ignore[method-assign]

        get_stop_info = GetStopInfo(emt_repository, stop_id, expected_lines)  # type: ignore
        with pytest.raises(APIResponseError, match=expected_error_message):
            await get_stop_info.execute()

    @pytest.mark.asyncio
    async def test_get_stop_info_when_no_lines_available(self) -> None:
        """Test getting stop info when no lines are available."""
        stop_id = 123
        expected_stop = TestData().a_stop(stop_id=stop_id, line_numbers=None)

        emt_repository = FakeEMTRepository()
        emt_repository.get_stop_info = AsyncMock(return_value=expected_stop)  # type: ignore[method-assign]
        get_stop_info = GetStopInfo(emt_repository, stop_id)  # type: ignore
        stop = await get_stop_info.execute()

        assert stop.stop_lines == expected_stop.stop_lines
