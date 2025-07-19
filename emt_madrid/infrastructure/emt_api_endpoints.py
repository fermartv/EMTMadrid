"""Endpoints for the EMT API."""


class Auth:
    LOGIN = {
        "description": "Endpoint to authenticate and get an access token.",
        "endpoint": "v1/mobilitylabs/user/login/",
        "method": "GET",
        "headers": {"email": "", "password": ""},
        "data": None,
        "responses": {
            "authentication_successful": "01",
            "invalid_password": "89",
            "user_does_not_exist": "92",
            "api_limit_exceeded": "98",
        },
    }


class Stops:
    DETAIL = {
        "description": "Most complete endpoint to get information about a bus stop.",
        "endpoint": "v1/transport/busemtmad/stops/{stop_id}/detail/",
        "method": "GET",
        "headers": {"accessToken": ""},
        "data": None,
        "responses": {
            "stop_data_retrieved": "00",
            "detail_not_available": "81",
            "stop_not_found": "90",
            "invalid_token": "80",
            "api_limit_exceeded": "98",
        },
    }

    ARROUNDSTOP = {
        "description": "Get information about stops around a specific stop.",
        "endpoint": "v2/transport/busemtmad/stops/arroundstop/{stop_id}/0/",
        "method": "GET",
        "headers": {"accessToken": ""},
        "data": None,
        "responses": {
            "stop_data_retrieved": "00",
            "stop_not_found": "01",
            "invalid_token": "80",
        },
    }

    ARRIVAL = {
        "description": "Get information about arrivals at a specific stop.",
        "endpoint": "v2/transport/busemtmad/stops/{stop_id}/arrives/",
        "method": "POST",
        "headers": {"accessToken": ""},
        "data": {"stopId": "", "Text_EstimationsRequired_YN": "Y"},
        "responses": {"arrivals_retrieved": "00", "stop_not_found": "80"},
    }
