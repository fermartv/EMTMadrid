"""Tests for the EMT Madrid wrapper."""


import asyncio
import logging

import pytest
from aiohttp import ClientError

from emt_madrid import EMTAPIWrapper
from tests.conftest import MockAsyncSession


@pytest.mark.parametrize(
    "email, password, status, exception, num_log_msgs",
    (
        ("email", "password", 200, None, 0),
        ("invalid_email", "password", 200, None, 1),
        ("email", "invalid_password", 200, None, 1),
        ("email", "password", 500, None, 1),
        ("email", "password", 200, asyncio.TimeoutError, 1),
        ("email", "password", 200, ClientError, 1),
    ),
)
@pytest.mark.asyncio
async def test_authenticate(
    email, password, status, exception, num_log_msgs, caplog
):  # pylint: disable=too-many-arguments
    """Test authentication throws an HTTP error."""
    mock_session = MockAsyncSession(status=status, exc=exception)
    with caplog.at_level(logging.WARNING):
        emt_api = EMTAPIWrapper(
            session=mock_session, email=email, password=password, stop_id="test"
        )
        token = await emt_api.authenticate()

        if (
            email == "email"
            and password == "password"
            and status == 200
            and exception is None
        ):
            assert token == "3bd5855a-ed3d-41d5-8b4b-182726f86031"
        assert len(caplog.messages) == num_log_msgs


@pytest.mark.parametrize(
    "token, stop_id, status, exception, num_log_msgs",
    (
        ("token", "72", 200, None, 0),
        ("token", "invalid_stop_id", 200, None, 1),
        ("invalid_token", "72", 200, None, 1),
        ("token", "72", 500, None, 1),
        ("token", "72", 200, asyncio.TimeoutError, 1),
        ("token", "72", 200, TimeoutError, 1),
        ("token", "72", 200, ClientError, 1),
    ),
)
@pytest.mark.asyncio
async def test_update_stop_info(
    token, stop_id, status, exception, num_log_msgs, caplog, mocker
):  # pylint: disable=too-many-arguments
    """Test authentication throws an HTTP error."""
    mock_session = MockAsyncSession(status=status, exc=exception)
    with caplog.at_level(logging.WARNING):
        emt_api = EMTAPIWrapper(
            session=mock_session, email="email", password="password", stop_id=stop_id
        )
        mocker.patch.object(emt_api, "_token", new=token)
        response = await emt_api.update_stop_info()
        assert len(caplog.messages) == num_log_msgs
        if token == "token" and stop_id == "72" and status == 200 and exception is None:
            assert response is not None
            assert response.get("stop_id") == "72"
            assert response.get("stop_name") == "Cibeles-Casa de América"
            assert (
                response.get("stop_address") == "Pº de Recoletos, 2 (Pza. de Cibeles)"
            )
            assert len(response.get("stop_coordinates")) == 2


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
    "token, stop_id, stop_info, status, exception, num_log_msgs",
    (
        ("token", "72", {}, 200, None, 0),
        ("token", "72", pre_loaded_stop_info, 200, None, 0),
        ("token", "invalid_stop_id", pre_loaded_stop_info, 200, None, 1),
        ("token", "invalid_stop_id", {}, 200, None, 1),
        ("invalid_token", "72", {}, 200, None, 1),
        ("token", "72", {}, 500, None, 1),
        ("token", "72", {}, 200, asyncio.TimeoutError, 1),
        ("token", "72", {}, 200, TimeoutError, 1),
        ("token", "72", {}, 200, ClientError, 1),
    ),
)
@pytest.mark.asyncio
async def test_update_bus_arrivals(
    token, stop_id, stop_info, status, exception, num_log_msgs, caplog, mocker
):  # pylint: disable=too-many-arguments
    """Test authentication throws an HTTP error."""

    mock_session = MockAsyncSession(status=status, exc=exception)
    with caplog.at_level(logging.WARNING):
        emt_api = EMTAPIWrapper(
            session=mock_session, email="email", password="password", stop_id=stop_id
        )
        mocker.patch.object(emt_api, "_token", new=token)
        if stop_info != {}:
            mocker.patch.object(emt_api, "_stop_info", new=stop_info)
        response = await emt_api.update_bus_arrivals()
        assert len(caplog.messages) == num_log_msgs
        if token == "token" and stop_id == "72" and status == 200 and exception is None:
            assert response is not None
            line = response["lines"]["27"]
            assert len(line.get("arrivals")) == 2
            assert len(line.get("distance")) == 2

            line = response["lines"]["53"]
            assert len(line.get("arrivals")) == 2
            assert len(line.get("distance")) == 2
