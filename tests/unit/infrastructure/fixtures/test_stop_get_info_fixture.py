from emt_madrid.domain.stop import Stop
from emt_madrid.domain.line import Line
from datetime import time
from emt_madrid.domain.day_type import DayType

STOP_ID = 72
STOP_NAME = "Cibeles-Casa de América"
STOP_ADDRESS = "Pº de Recoletos, 2 (Pza. de Cibeles)"
STOP_COORDINATES = [-3.69214452424823, 40.4203613685499]
STOP_LINES = [
    {
        "LINE_LABEL": "5",
        "MAX_FREQ": "19",
        "MIN_FREQ": "12",
        "ORIGIN": "SOL/SEVILLA",
        "DESTINATION": "CHAMARTIN",
        "START_TIME": "06:30",
        "END_TIME": "00:04",
        "DAY_TYPE": DayType.WORKING_DAY,
    },
    {
        "LINE_LABEL": "14",
        "MAX_FREQ": "15",
        "MIN_FREQ": "7",
        "ORIGIN": "CONDE DE CASAL",
        "DESTINATION": "PIO XII",
        "START_TIME": "06:20",
        "END_TIME": "23:36",
        "DAY_TYPE": DayType.FESTIVE,
    },
    {
        "LINE_LABEL": "15",
        "MAX_FREQ": "15",
        "MIN_FREQ": "7",
        "ORIGIN": "CONDE DE CASAL",
        "DESTINATION": "PIO XII",
        "START_TIME": "06:20",
        "END_TIME": "23:36",
        "DAY_TYPE": DayType.SATURDAY,
    },
]

STOP_GET_INFO_OK = Stop(
    stop_id=STOP_ID,
    stop_name=STOP_NAME,
    stop_address=STOP_ADDRESS,
    stop_coordinates=STOP_COORDINATES,
    stop_lines=[
        Line(
            line_number=STOP_LINES[0]["LINE_LABEL"],
            max_frequency=int(STOP_LINES[0]["MAX_FREQ"]),
            min_frequency=int(STOP_LINES[0]["MIN_FREQ"]),
            origin=STOP_LINES[0]["ORIGIN"],
            destination=STOP_LINES[0]["DESTINATION"],
            start_time=time.fromisoformat(STOP_LINES[0]["START_TIME"]),
            end_time=time.fromisoformat(STOP_LINES[0]["END_TIME"]),
            day_type=STOP_LINES[0]["DAY_TYPE"],
            arrival=None,
            next_arrival=None,
        ),
        Line(
            line_number=STOP_LINES[1]["LINE_LABEL"],
            max_frequency=int(STOP_LINES[1]["MAX_FREQ"]),
            min_frequency=int(STOP_LINES[1]["MIN_FREQ"]),
            origin=STOP_LINES[1]["ORIGIN"],
            destination=STOP_LINES[1]["DESTINATION"],
            start_time=time.fromisoformat(STOP_LINES[1]["START_TIME"]),
            end_time=time.fromisoformat(STOP_LINES[1]["END_TIME"]),
            day_type=STOP_LINES[1]["DAY_TYPE"],
            arrival=None,
            next_arrival=None,
        ),
        Line(
            line_number=STOP_LINES[2]["LINE_LABEL"],
            max_frequency=int(STOP_LINES[2]["MAX_FREQ"]),
            min_frequency=int(STOP_LINES[2]["MIN_FREQ"]),
            origin=STOP_LINES[2]["ORIGIN"],
            destination=STOP_LINES[2]["DESTINATION"],
            start_time=time.fromisoformat(STOP_LINES[2]["START_TIME"]),
            end_time=time.fromisoformat(STOP_LINES[2]["END_TIME"]),
            day_type=STOP_LINES[2]["DAY_TYPE"],
            arrival=None,
            next_arrival=None,
        ),
    ],
)

# Example response for endpoint "v1/transport/busemtmad/stops/{stop_id}/detail/"
STOP_GET_INFO_OK_RESPONSE = {
    "code": "00",
    "description": "Data recovered OK",
    "datetime": "2025-07-15T18:37:33.638842",
    "data": [
        {
            "stops": [
                {
                    "stop": str(STOP_ID),
                    "name": STOP_NAME,
                    "postalAddress": STOP_ADDRESS,
                    "geometry": {
                        "type": "Point",
                        "coordinates": STOP_COORDINATES,
                    },
                    "pmv": "60996",
                    "dataLine": [
                        {
                            "line": "005",
                            "label": STOP_LINES[0]["LINE_LABEL"],
                            "direction": "B",
                            "maxFreq": STOP_LINES[0]["MAX_FREQ"],
                            "minFreq": STOP_LINES[0]["MIN_FREQ"],
                            "headerA": STOP_LINES[0]["ORIGIN"],
                            "headerB": STOP_LINES[0]["DESTINATION"],
                            "startTime": STOP_LINES[0]["START_TIME"],
                            "stopTime": STOP_LINES[0]["END_TIME"],
                            "dayType": "LA",
                        },
                        {
                            "line": "014",
                            "label": STOP_LINES[1]["LINE_LABEL"],
                            "direction": "B",
                            "maxFreq": STOP_LINES[1]["MAX_FREQ"],
                            "minFreq": STOP_LINES[1]["MIN_FREQ"],
                            "headerA": STOP_LINES[1]["ORIGIN"],
                            "headerB": STOP_LINES[1]["DESTINATION"],
                            "startTime": STOP_LINES[1]["START_TIME"],
                            "stopTime": STOP_LINES[1]["END_TIME"],
                            "dayType": "FE",
                        },
                        {
                            "line": "015",
                            "label": STOP_LINES[2]["LINE_LABEL"],
                            "direction": "B",
                            "maxFreq": STOP_LINES[2]["MAX_FREQ"],
                            "minFreq": STOP_LINES[2]["MIN_FREQ"],
                            "headerA": STOP_LINES[2]["ORIGIN"],
                            "headerB": STOP_LINES[2]["DESTINATION"],
                            "startTime": STOP_LINES[2]["START_TIME"],
                            "stopTime": STOP_LINES[2]["END_TIME"],
                            "dayType": "SA",
                        },
                    ],
                }
            ]
        }
    ],
}

STOP_GET_INFO_NOT_FOUND_RESPONSE = {
    "code": "90",
    "description": "Error managing internal services",
    "datetime": "2025-07-15T19:09:47.928432",
    "data": [],
}

STOP_GET_INFO_DETAIL_NOT_AVAILABLE_RESPONSE = {
    "code": "81",
    "description": "No records found or error, (lapsed: 444 millsecs)",
    "datetime": "2023-07-18T16:49:03.435480",
    "data": [{}],
}

STOP_GET_INFO_NO_DATA_RESPONSE = {
    "code": "00",
    "description": "Data recovered OK",
    "datetime": "2025-07-15T18:37:33.638842",
}
