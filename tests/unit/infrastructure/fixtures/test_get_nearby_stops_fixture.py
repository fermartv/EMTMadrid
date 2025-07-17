from emt_madrid.domain.stop import Stop
from emt_madrid.domain.line import Line

STOP_ID = 72
STOP_NAME = "Cibeles-Casa de América"
STOP_ADDRESS = "Pº de Recoletos, 2 (Pza. de Cibeles)"
STOP_COORDINATES = [-3.69214452424823, 40.4203613685499]
STOP_LINES = [
    {
        "LINE_LABEL": "5",
        "ORIGIN": "SOL/SEVILLA",
        "DESTINATION": "CHAMARTIN",
    },
    {
        "LINE_LABEL": "14",
        "ORIGIN": "CONDE DE CASAL",
        "DESTINATION": "PIO XII",
    },
]

GET_NEARBY_STOPS_OK = Stop(
    stop_id=STOP_ID,
    stop_name=STOP_NAME,
    stop_address=STOP_ADDRESS,
    stop_coordinates=STOP_COORDINATES,
    stop_lines=[
        Line(
            line_number=STOP_LINES[0]["LINE_LABEL"],
            origin=STOP_LINES[0]["ORIGIN"],
            destination=STOP_LINES[0]["DESTINATION"],
            arrival=None,
            next_arrival=None,
        ),
        Line(
            line_number=STOP_LINES[1]["LINE_LABEL"],
            origin=STOP_LINES[1]["ORIGIN"],
            destination=STOP_LINES[1]["DESTINATION"],
            arrival=None,
            next_arrival=None,
        ),
    ],
)

# Example response for endpoint "v2/transport/busemtmad/stops/arroundstop/{stop_id}/0/"
GET_NEARBY_STOPS_OK_RESPONSE = {
    "code": "00",
    "description": "Data recovered OK (lapsed: 82 millsecs)",
    "data": [
        {
            "stopId": STOP_ID,
            "geometry": {
                "type": "Point",
                "coordinates": STOP_COORDINATES,
            },
            "stopName": STOP_NAME,
            "address": STOP_ADDRESS,
            "metersToPoint": 0,
            "lines": [
                {
                    "line": STOP_LINES[0]["LINE_LABEL"],
                    "label": STOP_LINES[0]["LINE_LABEL"],
                    "nameA": STOP_LINES[0]["ORIGIN"],
                    "nameB": STOP_LINES[0]["DESTINATION"],
                    "metersFromHeader": 8082,
                    "to": "B",
                },
                {
                    "line": STOP_LINES[1]["LINE_LABEL"],
                    "label": STOP_LINES[1]["LINE_LABEL"],
                    "nameA": STOP_LINES[1]["DESTINATION"],
                    "nameB": STOP_LINES[1]["ORIGIN"],
                    "metersFromHeader": 8082,
                    "to": "A",
                },
            ],
        }
    ],
}

GET_NEARBY_STOPS_NOT_FOUND_RESPONSE = {
    "code": "01",
    "description": "Error managing internal services",
    "datetime": "2025-07-15T19:09:47.928432",
    "data": [],
}

GET_NEARBY_STOPS_NO_DATA_RESPONSE = {
    "code": "00",
    "description": "Data recovered OK",
    "datetime": "2025-07-15T18:37:33.638842",
}
