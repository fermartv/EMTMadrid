"""Tests for the EMT Madrid wrapper."""


import logging

import pytest

from emt_madrid import EMTAPIWrapper
from tests.conftest import PRE_LOADED_STOP_INFO, MockAsyncSession, check_stop_info


@pytest.mark.parametrize(
    "email, password, num_log_msgs",
    (
        ("email", "password", 0),
        ("invalid_email", "password", 1),
        ("email", "invalid_password", 1),
    ),
)
@pytest.mark.asyncio
async def test_parse_token(
    email, password, num_log_msgs, caplog
):  # pylint: disable=too-many-arguments
    """Test parse_token function."""
    mock_session = MockAsyncSession()
    with caplog.at_level(logging.WARNING):
        emt_api = EMTAPIWrapper(
            session=mock_session, email=email, password=password, stop_id="test"
        )
        await emt_api.authenticate()

        if email == "email" and password == "password":
            assert emt_api.token == "3bd5855a-ed3d-41d5-8b4b-182726f86031"
        assert len(caplog.messages) == num_log_msgs


@pytest.mark.parametrize(
    "token, stop_id, num_log_msgs",
    (
        ("token", "72", 0),
        ("token", "invalid_stop_id", 1),
        ("invalid_token", "72", 1),
        ("invalid_token", "invalid_stop_id", 1),
        (None, "72", 1),
        ("token", None, 1),
        (None, None, 1),
    ),
)
@pytest.mark.asyncio
async def test_parse_stop(token, stop_id, num_log_msgs, caplog):
    """Test parse_stop and parse_lines functions."""
    mock_session = MockAsyncSession()
    with caplog.at_level(logging.WARNING):
        emt_api = EMTAPIWrapper(
            session=mock_session, email="email", password="password", stop_id=stop_id
        )
        emt_api.set_token(token)
        await emt_api.update_stop_info()
        stop_info = emt_api.get_stop_info()
        assert len(caplog.messages) == num_log_msgs
        if token == "token" and stop_id == "72":
            assert stop_info is not None
            assert stop_info.get("stop_id") == "72"
            assert stop_info.get("stop_name") == "Cibeles-Casa de América"
            assert (
                stop_info.get("stop_address") == "Pº de Recoletos, 2 (Pza. de Cibeles)"
            )
            assert len(stop_info.get("stop_coordinates")) == 2

            check_stop_info(stop_info)


@pytest.mark.parametrize(
    "token, stop_id, stop_info, num_log_msgs",
    (
        ("token", "72", {}, 0),
        ("token", "72", PRE_LOADED_STOP_INFO, 0),
        ("token", "invalid_stop_id", PRE_LOADED_STOP_INFO, 1),
        ("token", "invalid_stop_id", {}, 1),
        ("invalid_token", "72", {}, 1),
        ("invalid_token", "72", PRE_LOADED_STOP_INFO, 1),
        ("invalid_token", "invalid_stop_id", PRE_LOADED_STOP_INFO, 1),
        ("invalid_token", "invalid_stop_id", {}, 1),
    ),
)
@pytest.mark.asyncio
async def test_parse_arrivals(
    token, stop_id, stop_info, num_log_msgs, caplog, mocker
):  # pylint: disable=too-many-arguments
    """Test parse_arrivals function."""

    mock_session = MockAsyncSession()
    with caplog.at_level(logging.WARNING):
        emt_api = EMTAPIWrapper(
            session=mock_session, email="email", password="password", stop_id=stop_id
        )
        emt_api.set_token(token)
        if stop_info != {}:
            mocker.patch.object(emt_api, "_stop_info", new=stop_info)
        await emt_api.update_bus_arrivals()
        stop_info = emt_api.get_stop_info()
        assert len(caplog.messages) == num_log_msgs
        if token == "token" and stop_id == "72":
            assert stop_info is not None
            line = stop_info["lines"]["27"]
            assert len(line.get("arrivals")) == 2
            assert len(line.get("distance")) == 2

            line = stop_info["lines"]["53"]
            assert len(line.get("arrivals")) == 2
            assert len(line.get("distance")) == 2
