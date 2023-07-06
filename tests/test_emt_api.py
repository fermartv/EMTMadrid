"""Tests for the EMT Madrid wrapper."""


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
        ("email", "password", 200, TimeoutError, 1),
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
        emt_api = EMTAPIWrapper(session=mock_session, email=email, password=password)
        token = await emt_api.authenticate()

        if (
            email == "email"
            and password == "password"
            and status == 200
            and exception is None
        ):
            assert token == "3bd5855a-ed3d-41d5-8b4b-182726f86031"
        assert len(caplog.messages) == num_log_msgs
