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
        "ARRIVAL_SEC": 62,
        "ARRIVAL_MIN": 1,
        "NEXT_ARRIVAL_SEC": 241,
        "NEXT_ARRIVAL_MIN": 4,
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
        "ARRIVAL_SEC": 125,
        "ARRIVAL_MIN": 2,
        "NEXT_ARRIVAL_SEC": None,
        "NEXT_ARRIVAL_MIN": None,
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
        "ARRIVAL_SEC": None,
        "ARRIVAL_MIN": None,
        "NEXT_ARRIVAL_SEC": None,
        "NEXT_ARRIVAL_MIN": None,
    },
]

STOP_GET_ARRIVALS_OK = Stop(
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
            arrival=STOP_LINES[0]["ARRIVAL_MIN"],
            next_arrival=STOP_LINES[0]["NEXT_ARRIVAL_MIN"],
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
            arrival=STOP_LINES[1]["ARRIVAL_MIN"],
            next_arrival=STOP_LINES[1]["NEXT_ARRIVAL_MIN"],
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
            arrival=STOP_LINES[2]["ARRIVAL_MIN"],
            next_arrival=STOP_LINES[2]["NEXT_ARRIVAL_MIN"],
        ),
    ],
)

# Example response for endpoint "v2/transport/busemtmad/stops/{stop_id}/arrives/"
STOP_GET_ARRIVALS_OK_RESPONSE = {
    "code": "00",
    "description": " Data recovered  OK  (lapsed: 1065 millsecs)",
    "datetime": "2023-07-10T19:29:24.959411",
    "data": [
        {
            "Arrive": [
                {
                    "line": STOP_LINES[0]["LINE_LABEL"],
                    "stop": STOP_ID,
                    "isHead": "False",
                    "destination": STOP_LINES[0]["DESTINATION"],
                    "deviation": 0,
                    "bus": 532,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-3.692979009005247, 40.41863125675024],
                    },
                    "estimateArrive": STOP_LINES[0]["ARRIVAL_SEC"],
                    "DistanceBus": 25,
                    "positionTypeBus": "0",
                },
                {
                    "line": STOP_LINES[1]["LINE_LABEL"],
                    "stop": STOP_ID,
                    "isHead": "False",
                    "destination": STOP_LINES[1]["DESTINATION"],
                    "deviation": 0,
                    "bus": 2060,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-3.698281336673952, 40.41700397996393],
                    },
                    "estimateArrive": STOP_LINES[1]["ARRIVAL_SEC"],
                    "DistanceBus": 727,
                    "positionTypeBus": "0",
                },
                {
                    "line": STOP_LINES[0]["LINE_LABEL"],
                    "stop": STOP_ID,
                    "isHead": "False",
                    "destination": STOP_LINES[0]["DESTINATION"],
                    "deviation": 0,
                    "bus": 531,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-3.691569683861637, 40.408476053298756],
                    },
                    "estimateArrive": STOP_LINES[0]["NEXT_ARRIVAL_SEC"],
                    "DistanceBus": 955,
                    "positionTypeBus": "0",
                },
            ],
            "StopInfo": [],
            "ExtraInfo": [],
            "Incident": {},
        }
    ],
}

STOP_GET_ARRIVALS_NOT_FOUND_RESPONSE = {
    "code": "80",
    "description": [
        {"ES": "Parada no disponible actualmente o inexistente"},
        {"EN": "Bus Stop disabled or not exists"},
    ],
    "datetime": "2023-07-10T19:33:32.596198",
    "data": [{"Arrive": [], "StopInfo": [], "ExtraInfo": [], "Incident": {}}],
}

STOP_GET_ARRIVALS_NO_DATA_RESPONSE = {
    "code": "00",
    "description": " Data recovered  OK  (lapsed: 1065 millsecs)",
    "datetime": "2023-07-10T19:29:24.959411",
}
