"""Tests for the EMT Madrid wrapper."""


import asyncio
import logging

import pytest

from emt_madrid import EMTAPIAuthenticator, EMTAPIBusStop
from tests.conftest import MockAsyncSession, check_stop_info


@pytest.mark.asyncio
async def concurrent_calls(session, token, stop_id, status, exception):
    """Test function to simulate concurrent API calls."""
    emt_api_bus_stop = EMTAPIBusStop(session, token, stop_id)
    await emt_api_bus_stop.update_stop_info()
    await emt_api_bus_stop.update_bus_arrivals()
    stop_info = emt_api_bus_stop.get_stop_info()
    assert stop_info is not None
    if token is not None and stop_id == "72" and status == 200 and exception is None:
        check_stop_info(stop_info=stop_info, distance=2, arrivals=2)


async def run_concurrent_calls(
    email, password, stop_id, status, exception, call_count
):  # pylint: disable=too-many-arguments
    """Function to run the concurrent calls test."""
    mock_session = MockAsyncSession(status=status, exc=exception)
    async with mock_session as session:
        emt_api_authenticator = EMTAPIAuthenticator(session, email, password)
        await emt_api_authenticator.authenticate()
        token = emt_api_authenticator.token
        tasks = [
            concurrent_calls(session, token, stop_id, status, exception)
            for _ in range(1000)
        ]
        await asyncio.gather(*tasks)
        assert session.call_count == call_count


@pytest.mark.parametrize(
    "email, password, stop_id, status, exception, call_count, num_log_msgs",
    (
        ("email", "password", "72", 200, None, 2001, 0),
        ("invalid_email", "password", "72", 200, None, 1, 1001),
        ("email", "invalid_password", "72", 200, None, 1, 1001),
        ("email", "password", "invalid_stop_id", 200, None, 3001, 2000),
        ("email", "password", "72", 500, None, 1, 1001),
        ("email", "password", "72", 200, asyncio.TimeoutError, 1, 1001),
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
