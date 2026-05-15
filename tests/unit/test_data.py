from emt_madrid.domain.bus_arrival import BusArrival
from emt_madrid.domain.line import Line
from emt_madrid.domain.stop import Stop


class TestData:
    @staticmethod
    def a_stop(
        stop_id: int = 123,
        line_numbers: list[str] | None = None,
        stop_name: str = "Test Stop",
        stop_address: str = "Test Address",
        stop_coordinates: list[float] = [0, 0],
        bus_arrivals: list[BusArrival] | None = None,
    ) -> Stop:
        lines = [
            Line(
                line_number=str(num),
                origin="Test Origin",
                destination="Test Destination",
            )
            for num in (line_numbers or [])
        ]

        return Stop(
            stop_id=stop_id,
            stop_name=stop_name,
            stop_address=stop_address,
            stop_coordinates=stop_coordinates,
            stop_lines=lines,
            bus_arrivals=bus_arrivals or [],
        )

    @staticmethod
    def a_bus_arrival(
        line: str = "1",
        bus_id: int = 100,
        destination: str = "Test Destination",
        coordinates: list[float] = [0.0, 0.0],
        estimate_arrive_sec: int | None = None,
        distance_bus: int | None = None,
        is_head: bool = False,
        deviation: int = 0,
        position_type_bus: str = "0",
    ) -> BusArrival:
        return BusArrival(
            line=line,
            bus_id=bus_id,
            destination=destination,
            coordinates=coordinates,
            estimate_arrive_sec=estimate_arrive_sec,
            distance_bus=distance_bus,
            is_head=is_head,
            deviation=deviation,
            position_type_bus=position_type_bus,
        )
