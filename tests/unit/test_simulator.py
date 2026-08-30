from src.simulator.simulator import create_fleet


def test_create_fleet():
    fleet = create_fleet()

    assert len(fleet) == 10

    assert fleet[0].vehicle_id == "EV001"
    assert fleet[-1].vehicle_id == "EV010"

    assert fleet[0].driver_id == "DRV001"
    assert fleet[-1].driver_id == "DRV010"

    assert fleet[0].battery_soc_pct != fleet[-1].battery_soc_pct
    assert fleet[0].odometer_km != fleet[-1].odometer_km


def test_create_custom_fleet_size():
    fleet = create_fleet(3)

    assert len(fleet) == 3
    assert [vehicle.vehicle_id for vehicle in fleet] == [
        "EV001",
        "EV002",
        "EV003",
    ]
def test_simulate_tick_updates_moving_vehicle():
    from src.simulator.simulator import simulate_tick

    fleet = create_fleet(1)
    vehicle = fleet[0]

    vehicle.speed_kmh = 36.0

    original_odometer = vehicle.odometer_km
    original_soc = vehicle.battery_soc_pct
    original_rpm = vehicle.motor_rpm
    original_temperature = vehicle.motor_temperature_c

    simulate_tick(fleet, 1.0)

    assert vehicle.odometer_km > original_odometer
    assert vehicle.battery_soc_pct < original_soc
    assert vehicle.motor_rpm > original_rpm
    assert vehicle.motor_temperature_c > original_temperature
    assert vehicle.idle_duration_sec == 0

def test_generate_telemetry_events():
    from src.simulator.simulator import generate_telemetry_events

    fleet = create_fleet(3)

    for vehicle in fleet:
        vehicle.speed_kmh = 30.0

    events = generate_telemetry_events(fleet, 1.0)

    assert len(events) == 3

    assert len({event["event_id"] for event in events}) == 3

    assert {event["vehicle_id"] for event in events} == {
        "EV001",
        "EV002",
        "EV003",
    }

    for event in events:
        assert event["speed_kmh"] == 30.0
        assert event["battery_soc_pct"] < 100.0
        assert event["timestamp"]

class FakeProducer:
    def __init__(self):
        self.events = []

    def send(self, event: dict) -> None:
        self.events.append(event)


def test_publish_telemetry():
    from src.simulator.simulator import publish_telemetry

    fleet = create_fleet(3)

    for vehicle in fleet:
        vehicle.speed_kmh = 30.0

    producer = FakeProducer()

    published_count = publish_telemetry(
        fleet,
        producer,
        1.0,
    )

    assert published_count == 3
    assert len(producer.events) == 3
    assert {
        event["vehicle_id"]
        for event in producer.events
    } == {
        "EV001",
        "EV002",
        "EV003",
    }
def test_parse_args_defaults(monkeypatch):
    from src.simulator.__main__ import parse_args

    monkeypatch.setattr(
        "sys.argv",
        ["simulator"],
    )

    args = parse_args()

    assert args.vehicles == 10
    assert args.interval == 1.0


def test_parse_args_custom_values(monkeypatch):
    from src.simulator.__main__ import parse_args

    monkeypatch.setattr(
        "sys.argv",
        [
            "simulator",
            "--vehicles",
            "25",
            "--interval",
            "0.5",
        ],
    )

    args = parse_args()

    assert args.vehicles == 25
    assert args.interval == 0.5

import pytest


def test_main_rejects_zero_vehicles(monkeypatch):
    from src.simulator.__main__ import main

    monkeypatch.setattr(
        "sys.argv",
        ["simulator", "--vehicles", "0"],
    )

    with pytest.raises(ValueError, match="vehicles must be greater than zero"):
        main()


def test_main_rejects_negative_interval(monkeypatch):
    from src.simulator.__main__ import main

    monkeypatch.setattr(
        "sys.argv",
        ["simulator", "--interval", "-1"],
    )

    with pytest.raises(
        ValueError,
        match="interval must be greater than zero",
    ):
        main()