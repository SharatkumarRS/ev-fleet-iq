from src.simulator.vehicle_state import VehicleState


def create_test_vehicle() -> VehicleState:
    return VehicleState(
        vehicle_id="EV001",
        driver_id="DRV001",
        latitude=12.9716,
        longitude=77.5946,
        heading=90.0,
        speed_kmh=36.0,
        odometer_km=18342.7,
        battery_soc_pct=85.0,
        battery_voltage_v=400.0,
        battery_current_a=0.0,
        battery_temperature_c=30.0,
        motor_temperature_c=35.0,
        motor_rpm=0,
        brake_temperature_c=30.0,
        harsh_acceleration=False,
        harsh_braking=False,
        speeding=False,
        idle_duration_sec=0,
        order_id="ORD100245",
        route_id="RT50021",
        delivery_status="ASSIGNED",
    )


def test_vehicle_state_creation():
    vehicle = create_test_vehicle()

    assert vehicle.vehicle_id == "EV001"
    assert vehicle.driver_id == "DRV001"
    assert vehicle.speed_kmh == 36.0
    assert vehicle.battery_soc_pct == 85.0
    assert vehicle.motor_rpm == 0
    assert vehicle.delivery_status == "ASSIGNED"


def test_vehicle_movement():
    vehicle = create_test_vehicle()

    original_latitude = vehicle.latitude
    original_longitude = vehicle.longitude
    original_odometer = vehicle.odometer_km

    vehicle.update_position(1.0)

    assert vehicle.latitude == original_latitude
    assert vehicle.longitude > original_longitude
    assert vehicle.odometer_km > original_odometer
    assert round(vehicle.odometer_km - original_odometer, 5) == 0.01


def test_battery_consumption():
    vehicle = create_test_vehicle()

    original_soc = vehicle.battery_soc_pct

    vehicle.update_battery(10.0)

    assert vehicle.battery_soc_pct < original_soc
    assert round(original_soc - vehicle.battery_soc_pct, 5) == 3.66667


def test_battery_does_not_go_below_zero():
    vehicle = create_test_vehicle()
    vehicle.battery_soc_pct = 0.01

    vehicle.update_battery(1000.0)

    assert vehicle.battery_soc_pct == 0.0


def test_battery_does_not_change_for_zero_distance():
    vehicle = create_test_vehicle()

    original_soc = vehicle.battery_soc_pct

    vehicle.update_battery(0.0)

    assert vehicle.battery_soc_pct == original_soc


def test_motor_rpm_tracks_speed():
    vehicle = create_test_vehicle()

    vehicle.speed_kmh = 40.0
    vehicle.update_motor()

    assert vehicle.motor_rpm == 3200

    vehicle.speed_kmh = 0.0
    vehicle.update_motor()

    assert vehicle.motor_rpm == 0

def test_motor_temperature_changes_with_vehicle_state():
    vehicle = create_test_vehicle()

    original_temperature = vehicle.motor_temperature_c

    vehicle.speed_kmh = 40.0
    vehicle.update_motor_temperature()

    assert vehicle.motor_temperature_c > original_temperature

    vehicle.speed_kmh = 0.0
    vehicle.update_motor_temperature()

    assert vehicle.motor_temperature_c < original_temperature + 0.5
def test_harsh_acceleration():
    vehicle = create_test_vehicle()

    vehicle.speed_kmh = 40.0
    vehicle.apply_harsh_acceleration()

    assert vehicle.harsh_acceleration is True
    assert vehicle.speed_kmh == 55.0


def test_harsh_braking():
    vehicle = create_test_vehicle()

    vehicle.speed_kmh = 50.0
    original_brake_temperature = vehicle.brake_temperature_c

    vehicle.apply_harsh_braking()

    assert vehicle.harsh_braking is True
    assert vehicle.speed_kmh == 30.0
    assert vehicle.brake_temperature_c > original_brake_temperature


def test_speeding_status():
    vehicle = create_test_vehicle()

    vehicle.speed_kmh = 70.0
    vehicle.update_speeding_status()

    assert vehicle.speeding is True

    vehicle.speed_kmh = 50.0
    vehicle.update_speeding_status()

    assert vehicle.speeding is False

def test_idle_duration():
    vehicle = create_test_vehicle()

    vehicle.speed_kmh = 0.0

    vehicle.update_idle(5.0)
    assert vehicle.idle_duration_sec == 5

    vehicle.update_idle(10.0)
    assert vehicle.idle_duration_sec == 15

    vehicle.speed_kmh = 30.0
    vehicle.update_idle(1.0)

    assert vehicle.idle_duration_sec == 0

def test_to_telemetry():
    vehicle = create_test_vehicle()

    event = vehicle.to_telemetry(
        event_id="evt_test_000001",
        timestamp="2026-08-29T07:30:00Z",
    )

    assert event["event_id"] == "evt_test_000001"
    assert event["vehicle_id"] == "EV001"
    assert event["driver_id"] == "DRV001"
    assert event["speed_kmh"] == 36.0
    assert event["battery_soc_pct"] == 85.0
    assert event["delivery_status"] == "ASSIGNED"

    assert len(event) == 22

def test_to_telemetry_matches_schema():
    import json
    from pathlib import Path

    from jsonschema import validate

    vehicle = create_test_vehicle()

    event = vehicle.to_telemetry(
        event_id="evt_test_000002",
        timestamp="2026-08-29T07:30:00Z",
    )

    schema_path = (
        Path(__file__).resolve().parents[2]
        / "schemas"
        / "telemetry"
        / "vehicle_telemetry_v1.json"
    )

    with schema_path.open(encoding="utf-8") as file:
        schema = json.load(file)

    validate(instance=event, schema=schema)