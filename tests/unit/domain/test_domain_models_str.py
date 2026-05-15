"""Tests for __str__ methods in domain models."""

from emt_madrid.domain.day_type import DayType
from emt_madrid.domain.line import Line
from tests.unit.test_data import TestData


class TestStopStr:
    """Test cases for Stop.__str__ method."""

    def test_stop_str_without_bus_arrivals(self) -> None:
        """Test Stop string representation without bus arrivals."""
        stop = TestData().a_stop(
            stop_id=123,
            stop_name="Test Stop",
            stop_address="Test Address",
            stop_coordinates=[-3.692, 40.42],
            line_numbers=["1", "2"],
        )
        result = str(stop)

        assert "Stop 123 - Test Stop at Test Address" in result
        assert "Coordinates: [-3.692, 40.42]" in result
        assert "Lines:" in result
        assert "Bus Arrivals:" not in result

    def test_stop_str_with_bus_arrivals(self) -> None:
        """Test Stop string representation with bus arrivals."""
        bus_arrivals = [
            TestData().a_bus_arrival(
                line="1",
                bus_id=100,
                destination="Destination A",
                coordinates=[-3.692, 40.420],
                estimate_arrive_sec=60,
            ),
            TestData().a_bus_arrival(
                line="2",
                bus_id=200,
                destination="Destination B",
                coordinates=[-3.693, 40.421],
                estimate_arrive_sec=120,
            ),
        ]
        stop = TestData().a_stop(
            stop_id=456,
            stop_name="Another Stop",
            stop_address="Another Address",
            stop_coordinates=[-3.693, 40.421],
            line_numbers=["1", "2"],
            bus_arrivals=bus_arrivals,
        )
        result = str(stop)

        assert "Stop 456 - Another Stop at Another Address" in result
        assert "Coordinates: [-3.693, 40.421]" in result
        assert "Bus Arrivals:" in result
        assert "Bus 100 (Line 1) → Destination A in 60s at [-3.692, 40.42]" in result
        assert "Bus 200 (Line 2) → Destination B in 120s at [-3.693, 40.421]" in result

    def test_stop_str_with_empty_bus_arrivals(self) -> None:
        """Test Stop string representation with empty bus arrivals list."""
        stop = TestData().a_stop(
            stop_id=789,
            stop_name="Empty Arrivals Stop",
            stop_address="Empty Address",
            stop_coordinates=[0, 0],
            line_numbers=[],
            bus_arrivals=[],
        )
        result = str(stop)

        assert "Stop 789 - Empty Arrivals Stop at Empty Address" in result
        assert "Bus Arrivals:" not in result


class TestLineStr:
    """Test cases for Line.__str__ method."""

    def test_line_str_with_arrivals(self) -> None:
        """Test Line string representation with arrival times."""
        line = Line(
            line_number="5",
            origin="SOL/SEVILLA",
            destination="CHAMARTIN",
            arrival=1,
            next_arrival=4,
        )
        result = str(line)
        assert result == "Line 5: SOL/SEVILLA → CHAMARTIN - 1 min - 4 min"

    def test_line_str_without_arrivals(self) -> None:
        """Test Line string representation without arrival times."""
        line = Line(
            line_number="14",
            origin="CONDE DE CASAL",
            destination="PIO XII",
            arrival=None,
            next_arrival=None,
        )
        result = str(line)
        assert result == "Line 14: CONDE DE CASAL → PIO XII - None min - None min"

    def test_line_str_with_only_first_arrival(self) -> None:
        """Test Line string representation with only first arrival."""
        line = Line(
            line_number="1",
            origin="Origin",
            destination="Destination",
            arrival=2,
            next_arrival=None,
        )
        result = str(line)
        assert result == "Line 1: Origin → Destination - 2 min - None min"


class TestDayTypeStr:
    """Test cases for DayType.__str__ method."""

    def test_working_day_str(self) -> None:
        """Test WORKING_DAY string representation."""
        assert str(DayType.WORKING_DAY) == "Working day"

    def test_saturday_str(self) -> None:
        """Test SATURDAY string representation."""
        assert str(DayType.SATURDAY) == "Saturday"

    def test_festive_str(self) -> None:
        """Test FESTIVE string representation."""
        assert str(DayType.FESTIVE) == "Festive"


class TestBusArrivalStr:
    """Test cases for BusArrival.__str__ method."""

    def test_bus_arrival_str_with_estimate(self) -> None:
        """Test BusArrival string representation with estimate_arrive_sec."""
        arrival = TestData().a_bus_arrival(
            line="5",
            bus_id=532,
            destination="CHAMARTIN",
            coordinates=[-3.692979, 40.418631],
            estimate_arrive_sec=62,
        )
        result = str(arrival)

        assert "Bus 532 (Line 5) → CHAMARTIN in 62s at [-3.692979, 40.418631]" == result

    def test_bus_arrival_str_without_estimate(self) -> None:
        """Test BusArrival string representation without estimate_arrive_sec."""
        arrival = TestData().a_bus_arrival(
            line="14",
            bus_id=2060,
            destination="PIO XII",
            coordinates=[-3.698281, 40.417004],
            estimate_arrive_sec=None,
        )
        result = str(arrival)

        assert (
            "Bus 2060 (Line 14) → PIO XII in Nones at [-3.698281, 40.417004]" == result
        )
