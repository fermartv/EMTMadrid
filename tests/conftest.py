"""EMT Madrid API tests configuration."""

import json
import pathlib
from typing import Any, Dict

TEST_EXAMPLES_PATH = pathlib.Path(__file__).parent / "response_examples"

_FIXTURE_LOGIN_OK = "LOGIN_OK.json"
_FIXTURE_LOGIN_INVALID_USER = "LOGIN_INVALID_USER.json"
_FIXTURE_LOGIN_INVALID_PASSWORD = "LOGIN_INVALID_PASSWORD.json"


class MockAsyncSession:
    """Mock GET requests to esios API."""

    status: int = 200
    _counter: int = 0
    _raw_response = None

    def __aenter__(self):
        """Return the async session as a context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Handle any exceptions raised within the context of the async session."""

    def __await__(self):
        """Allow the async session to be used with await statements."""
        yield
        return self

    async def close(self, *_args):
        """Close the session asynchronously."""

    def __init__(self, status=200, exc=None):
        """Set up desired mock response."""
        self.status = status
        self.exc = exc
        self._raw_response = {}

    async def json(self, *_args, **_kwargs):
        """Dumb await."""
        return self._raw_response

    async def get(self, url: str, headers: Dict[str, Any], *_args, **_kwargs):
        """Dumb await."""
        if self.exc:
            raise self.exc
        if url == "https://openapi.emtmadrid.es/v1/mobilitylabs/user/login/":
            if headers["email"] == "invalid_email":
                self._raw_response = load_fixture(_FIXTURE_LOGIN_INVALID_USER)
            elif headers["password"] == "invalid_password":
                self._raw_response = load_fixture(_FIXTURE_LOGIN_INVALID_PASSWORD)
            else:
                self._raw_response = load_fixture(_FIXTURE_LOGIN_OK)

        return self


def load_fixture(filename: str):
    """Load stored example for EMT API response."""
    return json.loads((TEST_EXAMPLES_PATH / filename).read_text())
