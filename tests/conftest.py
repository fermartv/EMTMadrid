"""EMT Madrid API tests configuration."""

import json
import pathlib
from typing import Any, Dict, Optional

TEST_EXAMPLES_PATH = pathlib.Path(__file__).parent / "response_examples"

_FIXTURE_LOGIN_OK = "LOGIN_OK.json"
_FIXTURE_LOGIN_INVALID_USER = "LOGIN_INVALID_USER.json"
_FIXTURE_LOGIN_INVALID_PASSWORD = "LOGIN_INVALID_PASSWORD.json"
_FIXTURE_STOP_DETAIL_OK = "STOP_DETAIL_OK.json"
_FIXTURE_STOP_DETAIL_INVALID_STOP = "STOP_DETAIL_INVALID_STOP.json"
_FIXTURE_STOP_DETAIL_INVALID_TOKEN = "STOP_DETAIL_INVALID_TOKEN.json"
_FIXTURE_STOP_ARRIVAL_OK = "STOP_ARRIVAL_OK.json"
_FIXTURE_STOP_ARRIVAL_INVALID_STOP = "STOP_ARRIVAL_INVALID_STOP.json"
_FIXTURE_STOP_ARRIVAL_INVALID_TOKEN = "STOP_ARRIVAL_INVALID_TOKEN.json"
_FIXTURE_API_LIMIT = "API_LIMIT.json"
_FIXTURE_STOP_INFO = "STOP_INFO.json"


class MockAsyncSession:
    """Mock GET requests to esios API."""

    status: int = 200
    _counter: int = 0
    _raw_response: Optional[Dict[str, Any]] = None

    def __aenter__(self):
        """Return the async session as a context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Handle any exceptions raised within the context of the async session."""

    def __await__(self):
        """Allow the async session to be used with await statements."""
        yield
        return self

    def __init__(self, status=200, exc=None):
        """Set up desired mock response."""
        self.status = status
        self.exc = exc
        self._raw_response = {}

    async def json(self, *_args, **_kwargs):
        """Dumb response."""
        return self._raw_response

    async def get(self, url: str, headers: Dict[str, Any], *_args, **_kwargs):
        """Dumb get method."""
        self._counter += 1
        if self.exc:
            raise self.exc
        if "user/login/" in url:
            if headers["email"] == "invalid_email":
                self._raw_response = load_fixture(_FIXTURE_LOGIN_INVALID_USER)
            elif headers["password"] == "invalid_password":
                self._raw_response = load_fixture(_FIXTURE_LOGIN_INVALID_PASSWORD)
            elif headers["password"] == "api_limit":
                self._raw_response = load_fixture(_FIXTURE_API_LIMIT)
            else:
                self._raw_response = load_fixture(_FIXTURE_LOGIN_OK)

        elif "stops" in url and "detail" in url:
            stop_id = url.split("/")[-3]
            if (
                headers["accessToken"] == "invalid_token"
                or headers["accessToken"] is None
            ):
                self._raw_response = load_fixture(_FIXTURE_STOP_DETAIL_INVALID_TOKEN)
            elif headers["accessToken"] == "api_limit":
                self._raw_response = load_fixture(_FIXTURE_API_LIMIT)
            elif stop_id in ("invalid_stop_id", "None"):
                self._raw_response = load_fixture(_FIXTURE_STOP_DETAIL_INVALID_STOP)
            else:
                self._raw_response = load_fixture(_FIXTURE_STOP_DETAIL_OK)
        return self

    async def post(self, url: str, headers: Dict[str, Any], *_args, **_kwargs):
        """Dumb post method."""
        self._counter += 1
        if self.exc:
            raise self.exc
        if "stops" in url and "arrives" in url:
            if headers["accessToken"] == "invalid_token":
                self._raw_response = load_fixture(_FIXTURE_STOP_ARRIVAL_INVALID_TOKEN)
            elif headers["accessToken"] == "api_limit":
                self._raw_response = load_fixture(_FIXTURE_API_LIMIT)
            elif url.split("/")[-3] == "invalid_stop_id":
                self._raw_response = load_fixture(_FIXTURE_STOP_ARRIVAL_INVALID_STOP)
            else:
                self._raw_response = load_fixture(_FIXTURE_STOP_ARRIVAL_OK)

        return self

    @property
    def call_count(self) -> int:
        """Return call counter."""
        return self._counter


def load_fixture(filename: str):
    """Load stored example for EMT API response."""
    return json.loads((TEST_EXAMPLES_PATH / filename).read_text())


def check_stop_info(stop_info, distance=0, arrivals=0):
    """Verify that the stop_info is correct."""
    lines = stop_info.get("lines")
    assert len(lines) == 12
    line = lines.get("27")
    assert line.get("destination") == "PLAZA CASTILLA"
    assert line.get("origin") == "EMBAJADORES"
    assert line.get("max_freq") == 11
    assert line.get("min_freq") == 3
    assert line.get("start_time") == "05:35"
    assert line.get("end_time") == "00:01"
    assert line.get("day_type") == "LA"
    assert len(line.get("distance")) == distance
    assert len(line.get("arrivals")) == arrivals
