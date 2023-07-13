"""Tests for the EMT Madrid wrapper."""


import asyncio
import logging

import pytest
from aiohttp import ClientError

from emt_madrid import EMTAPIAuthenticator, EMTAPIBusStop
from tests.conftest import _FIXTURE_STOP_INFO, MockAsyncSession, load_fixture

PRE_LOADED_STOP_INFO = load_fixture(_FIXTURE_STOP_INFO)


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
        emt_api = EMTAPIAuthenticator(
            session=mock_session, email="email", password="password"
        )
        await emt_api.authenticate()
        assert len(caplog.messages) == num_log_msgs
        assert mock_session.call_count == 1


@pytest.mark.parametrize(
    "token, status, exception, num_log_msgs, call_count",
    (
        ("token", 200, None, 0, 1),
        ("invalid_token", 200, None, 1, 1),
        ("api_limit", 200, None, 1, 1),
        ("token", 500, None, 1, 1),
        ("token", 200, asyncio.TimeoutError, 1, 1),
        ("token", 200, TimeoutError, 1, 1),
        ("token", 200, ClientError, 1, 1),
    ),
)
@pytest.mark.asyncio
async def test_update_stop_info(
    token, status, exception, num_log_msgs, call_count, caplog
):  # pylint: disable=too-many-arguments
    """Test update_stop_info method."""
    mock_session = MockAsyncSession(status=status, exc=exception)
    with caplog.at_level(logging.WARNING):
        emt_api = EMTAPIBusStop(session=mock_session, token=token, stop_id="72")
        await emt_api.update_stop_info()
        assert len(caplog.messages) == num_log_msgs
        assert mock_session.call_count == call_count


@pytest.mark.parametrize(
    "token, stop_info, status, exception, num_log_msgs, call_count",
    (
        ("token", {}, 200, None, 0, 2),
        ("token", PRE_LOADED_STOP_INFO, 200, None, 0, 1),
        ("api_limit", {}, 200, None, 1, 2),
        ("api_limit", PRE_LOADED_STOP_INFO, 200, None, 1, 1),
        ("invalid_token", PRE_LOADED_STOP_INFO, 200, None, 1, 1),
        ("invalid_token", {}, 200, None, 1, 2),
        (None, PRE_LOADED_STOP_INFO, 200, None, 1, 0),
        (None, {}, 200, None, 1, 0),
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
        emt_api_bus_stop = EMTAPIBusStop(
            session=mock_session, token=token, stop_id="72"
        )
        if stop_info != {}:
            mocker.patch.object(emt_api_bus_stop, "_stop_info", new=stop_info)
        await emt_api_bus_stop.update_bus_arrivals()
        assert len(caplog.messages) == num_log_msgs
        assert mock_session.call_count == call_count


@pytest.mark.asyncio
async def test_set_token():
    """Test set_token method."""
    mock_session = MockAsyncSession()
    emt_api_bus_stop = EMTAPIBusStop(
        session=mock_session, token="old_token", stop_id="72"
    )
    assert emt_api_bus_stop.token == "old_token"
    emt_api_bus_stop.set_token("new_token")
    assert emt_api_bus_stop.token == "new_token"


@pytest.mark.parametrize(
    "stop_info, line, num_log_msgs",
    (
        (PRE_LOADED_STOP_INFO, "27", 0),
        (PRE_LOADED_STOP_INFO, "C03", 0),
        (PRE_LOADED_STOP_INFO, "N25", 0),
        ({}, "27", 1),
        (PRE_LOADED_STOP_INFO, "invalid_line", 1),
    ),
)
@pytest.mark.asyncio
async def test_get_arrival_time(stop_info, line, num_log_msgs, caplog, mocker):
    """Test get_arrival_time method."""
    mock_session = MockAsyncSession()
    with caplog.at_level(logging.WARNING):
        emt_api_bus_stop = EMTAPIBusStop(
            session=mock_session, token="token", stop_id="72"
        )
        if stop_info != {}:
            mocker.patch.object(emt_api_bus_stop, "_stop_info", new=stop_info)
        emt_api_bus_stop.get_arrival_time(line)
        assert len(caplog.messages) == num_log_msgs


@pytest.mark.parametrize(
    "stop_info, line, num_log_msgs",
    (
        (PRE_LOADED_STOP_INFO, "27", 0),
        (PRE_LOADED_STOP_INFO, "C03", 0),
        (PRE_LOADED_STOP_INFO, "N25", 0),
        ({}, "27", 1),
        (PRE_LOADED_STOP_INFO, "invalid_line", 1),
    ),
)
@pytest.mark.asyncio
async def test_get_line_info(stop_info, line, num_log_msgs, caplog, mocker):
    """Test get_line_info method."""
    mock_session = MockAsyncSession()
    with caplog.at_level(logging.WARNING):
        emt_api_bus_stop = EMTAPIBusStop(
            session=mock_session, token="token", stop_id="72"
        )
        if stop_info != {}:
            mocker.patch.object(emt_api_bus_stop, "_stop_info", new=stop_info)
        emt_api_bus_stop.get_line_info(line)
        assert len(caplog.messages) == num_log_msgs
