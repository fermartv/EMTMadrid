"""Tests for the EMT Madrid wrapper."""

from unittest.mock import Mock, patch

import pytest

from emt_madrid.emt_madrid import APIEMT

VALID_LOGIN = {
    "code": "01",
    "description": "Token 3bd5855a-ed3d-41d5-8b4b-182726f86031",
    "datetime": "2023-06-29T19:50:08.307475",
    "data": [
        {
            "accessToken": "3bd5855a-ed3d-41d5-8b4b-182726f86031",
        }
    ],
}

VALID_STOP_INFO = {
    "code": "00",
    "description": "Data recovered  OK, (lapsed: 463 millsecs)",
    "datetime": "2023-07-02T15:41:44.008245",
    "data": [
        {
            "stops": [
                {
                    "stop": "72",
                    "name": "Cibeles-Casa de América",
                    "postalAddress": "Pº de Recoletos, 2 (Pza. de Cibeles)",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-3.69214452424823, 40.4203613685499],
                    },
                    "pmv": "60996",
                    "dataLine": [
                        {
                            "line": "005",
                            "label": "5",
                            "direction": "B",
                            "maxFreq": "33",
                            "minFreq": "16",
                            "headerA": "SOL/SEVILLA",
                            "headerB": "CHAMARTIN",
                            "startTime": "07:00",
                            "stopTime": "22:58",
                            "dayType": "FE",
                        },
                        {
                            "line": "027",
                            "label": "27",
                            "direction": "B",
                            "maxFreq": "25",
                            "minFreq": "11",
                            "headerA": "EMBAJADORES",
                            "headerB": "PLAZA CASTILLA",
                            "startTime": "07:00",
                            "stopTime": "00:01",
                            "dayType": "FE",
                        },
                        {
                            "line": "526",
                            "label": "N26",
                            "direction": "A",
                            "maxFreq": "60",
                            "minFreq": "20",
                            "headerA": "ALONSO MARTINEZ",
                            "headerB": "ALUCHE",
                            "startTime": "00:00",
                            "stopTime": "05:10",
                            "dayType": "FE",
                        },
                    ],
                }
            ]
        }
    ],
}


class TestAPIEMT:
    """Test for APIEMT class."""

    @pytest.fixture
    def api_emt(self) -> APIEMT:
        """Fixture for creating an APIEMT instance."""
        return APIEMT("user", "password", 72)

    @patch("requests.request")
    def test_authenticate_valid_credentials(self, request_mock: Mock, api_emt):
        """Test authentication with valid credentials."""
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = VALID_LOGIN
        request_mock.return_value = response_mock

        token = api_emt.authenticate()

        assert token == "3bd5855a-ed3d-41d5-8b4b-182726f86031"

    @patch("requests.request")
    def test_authenticate_http_error(self, request_mock: Mock, api_emt):
        """Test authentication throws an HTTP error."""
        response_mock = Mock(status_code=500)
        request_mock.return_value = response_mock

        token = api_emt.authenticate()

        assert token == "Invalid token"

    @patch("requests.request")
    def test_update_stop_info_valid_stop_id(self, request_mock: Mock, api_emt):
        """Test updating and retrieving stop information with a valid stop ID."""
        response_mock = Mock(status_code=200)
        response_mock.json.return_value = VALID_STOP_INFO
        request_mock.return_value = response_mock

        api_emt.update_stop_info()
        stop_info = api_emt.get_stop_info()

        assert stop_info.get("bus_stop_id") == 72
        assert stop_info.get("bus_stop_name") == "Cibeles-Casa de América"
        assert stop_info.get("bus_stop_coordinates") == [
            -3.69214452424823,
            40.4203613685499,
        ]
        assert (
            stop_info.get("bus_stop_address") == "Pº de Recoletos, 2 (Pza. de Cibeles)"
        )

        assert stop_info.get("lines").get("5").get("destination") == "CHAMARTIN"
        assert stop_info.get("lines").get("5").get("origin") == "SOL/SEVILLA"
        assert stop_info.get("lines").get("5").get("max_freq") == 33
        assert stop_info.get("lines").get("5").get("min_freq") == 16
        assert stop_info.get("lines").get("5").get("start_time") == "07:00"
        assert stop_info.get("lines").get("5").get("end_time") == "22:58"
        assert stop_info.get("lines").get("5").get("day_type") == "FE"
        assert stop_info.get("lines").get("5").get("distance") == []
        assert stop_info.get("lines").get("5").get("arrivals") == []

        assert stop_info.get("lines").get("27").get("destination") == "PLAZA CASTILLA"
        assert stop_info.get("lines").get("27").get("origin") == "EMBAJADORES"
        assert stop_info.get("lines").get("27").get("max_freq") == 25
        assert stop_info.get("lines").get("27").get("min_freq") == 11
        assert stop_info.get("lines").get("27").get("start_time") == "07:00"
        assert stop_info.get("lines").get("27").get("end_time") == "00:01"
        assert stop_info.get("lines").get("27").get("day_type") == "FE"
        assert stop_info.get("lines").get("27").get("distance") == []
        assert stop_info.get("lines").get("27").get("arrivals") == []

        assert stop_info.get("lines").get("N26").get("destination") == "ALONSO MARTINEZ"
        assert stop_info.get("lines").get("N26").get("origin") == "ALUCHE"
        assert stop_info.get("lines").get("N26").get("max_freq") == 60
        assert stop_info.get("lines").get("N26").get("min_freq") == 20
        assert stop_info.get("lines").get("N26").get("start_time") == "00:00"
        assert stop_info.get("lines").get("N26").get("end_time") == "05:10"
        assert stop_info.get("lines").get("N26").get("day_type") == "FE"
        assert stop_info.get("lines").get("N26").get("distance") == []
        assert stop_info.get("lines").get("N26").get("arrivals") == []


if __name__ == "__main__":
    pytest.main()
