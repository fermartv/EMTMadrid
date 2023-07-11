"""Tests for the EMT Madrid wrapper."""


import asyncio
import logging

import pytest
from aiohttp import ClientError

from emt_madrid import EMTAPIWrapper
from tests.conftest import MockAsyncSession


@pytest.mark.parametrize(
    "status, exception, num_log_msgs",
    (
        (200, None, 0),
        (500, None, 1),
        (200, asyncio.TimeoutError, 1),
        (200, TimeoutError, 1),
        (200, ClientError, 1),
    ),
)
@pytest.mark.asyncio
async def test_authenticate(status, exception, num_log_msgs, caplog):
    """Test authentication method."""
    mock_session = MockAsyncSession(status=status, exc=exception)
    with caplog.at_level(logging.WARNING):
        emt_api = EMTAPIWrapper(
            session=mock_session, email="email", password="password", stop_id="test"
        )
        await emt_api.authenticate()
        assert len(caplog.messages) == num_log_msgs
        assert mock_session.call_count == 1


@pytest.mark.parametrize(
    "token, status, exception, num_log_msgs, call_count",
    (
        ("token", 200, None, 0, 1),
        (None, 200, None, 1, 2),
        ("invalid_token", 200, None, 1, 2),
        ("token", 500, None, 1, 1),
        ("token", 200, asyncio.TimeoutError, 1, 1),
        ("token", 200, TimeoutError, 1, 1),
        ("token", 200, ClientError, 1, 1),
    ),
)
@pytest.mark.asyncio
async def test_update_stop_info(
    token, status, exception, num_log_msgs, call_count, caplog, mocker
):  # pylint: disable=too-many-arguments
    """Test update_stop_info method."""
    mock_session = MockAsyncSession(status=status, exc=exception)
    with caplog.at_level(logging.WARNING):
        emt_api = EMTAPIWrapper(
            session=mock_session, email="email", password="password", stop_id="72"
        )
        mocker.patch.object(emt_api, "_token", new=token)
        await emt_api.update_stop_info()
        assert len(caplog.messages) == num_log_msgs
        assert mock_session.call_count == call_count


pre_loaded_stop_info = {
    "lines": {
        "27": {
            "distance": [],
            "arrivals": [],
        },
        "53": {
            "distance": [],
            "arrivals": [],
        },
    },
}


@pytest.mark.parametrize(
    "token, stop_info, status, exception, num_log_msgs, call_count",
    (
        ("token", {}, 200, None, 0, 2),
        ("token", pre_loaded_stop_info, 200, None, 0, 1),
        ("invalid_token", pre_loaded_stop_info, 200, None, 1, 2),
        ("invalid_token", {}, 200, None, 1, 3),
        ("token", {}, 500, None, 1, 1),
        ("token", {}, 200, asyncio.TimeoutError, 1, 1),
        ("token", {}, 200, TimeoutError, 1, 1),
        ("token", {}, 200, ClientError, 1, 1),
    ),
)
@pytest.mark.asyncio
async def test_update_bus_arrivals(
    token, stop_info, status, exception, num_log_msgs, call_count, caplog, mocker
):  # pylint: disable=too-many-arguments
    """Test update_bus_arrivals method."""
    mock_session = MockAsyncSession(status=status, exc=exception)
    with caplog.at_level(logging.WARNING):
        emt_api = EMTAPIWrapper(
            session=mock_session, email="email", password="password", stop_id="72"
        )
        mocker.patch.object(emt_api, "_token", new=token)
        if stop_info != {}:
            mocker.patch.object(emt_api, "_stop_info", new=stop_info)
        await emt_api.update_bus_arrivals()
        assert len(caplog.messages) == num_log_msgs
        assert mock_session.call_count == call_count
