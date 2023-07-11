"""Tests for the EMT Madrid wrapper."""


import asyncio
import logging

import pytest

from emt_madrid import EMTAPIWrapper
from tests.conftest import MockAsyncSession


@pytest.mark.asyncio
async def concurrent_calls(
    email, password, stop_id, status, exception, call_count
):  # pylint: disable=too-many-arguments
    """Test function to simulate concurrent API calls."""
    mock_session = MockAsyncSession(status=status, exc=exception)
    async with mock_session as session:
        emt_api = EMTAPIWrapper(session, email, password, stop_id)
        await emt_api.authenticate()
        await emt_api.update_stop_info()
        await emt_api.update_bus_arrivals()
        stop_info = emt_api.get_stop_info()
        assert stop_info is not None
        assert mock_session.call_count == call_count


async def run_concurrent_calls(
    email, password, stop_id, status, exception, call_count
):  # pylint: disable=too-many-arguments
    """Function to run the concurrent calls test."""
    tasks = [
        concurrent_calls(email, password, stop_id, status, exception, call_count)
        for _ in range(1000)
    ]
    await asyncio.gather(*tasks)


@pytest.mark.parametrize(
    "email, password, stop_id, status, exception, call_count, num_log_msgs",
    (
        ("email", "password", "72", 200, None, 3, 0),
        ("invalid_email", "password", "72", 200, None, 6, 5000),
        ("email", "invalid_password", "72", 200, None, 6, 5000),
        ("email", "password", "invalid_stop_id", 200, None, 4, 2000),
        ("email", "password", "72", 500, None, 3, 3000),
        ("email", "password", "72", 200, asyncio.TimeoutError, 3, 3000),
    ),
)
def test_run_concurrent_calls(
    email, password, stop_id, status, exception, call_count, num_log_msgs, caplog
):  # pylint: disable=too-many-arguments
    """Test function to run the concurrent calls test."""
    with caplog.at_level(logging.WARNING):
        asyncio.run(
            run_concurrent_calls(
                email, password, stop_id, status, exception, call_count
            )
        )
        assert len(caplog.messages) == num_log_msgs
