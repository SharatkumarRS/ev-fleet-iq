from src.simulator.vehicle_state import VehicleState
from datetime import datetime, timezone
from uuid import uuid4
from src.ingestion.kafka_producer import VehicleTelemetryProducer


def create_fleet(vehicle_count: int = 10) -> list[VehicleState]:
    """Create the initial EV fleet."""

    fleet = []

    for index in range(1, vehicle_count + 1):
        vehicle = VehicleState(
            vehicle_id=f"EV{index:03d}",
            driver_id=f"DRV{index:03d}",
            latitude=12.85 + (index * 0.02),
            longitude=77.45 + (index * 0.02),
            heading=90.0,
            speed_kmh=0.0,
            odometer_km=10000.0 + (index * 500),
            battery_soc_pct=70.0 + (index * 2),
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
            order_id=f"ORD{100000 + index}",
            route_id=f"RT{50000 + index}",
            delivery_status="ASSIGNED",
        )

        fleet.append(vehicle)

    return fleet
def simulate_tick(
    fleet: list[VehicleState],
    elapsed_seconds: float = 1.0,
) -> None:
    """Advance every vehicle by one simulation tick."""

    for vehicle in fleet:
        distance_km = vehicle.update_position(elapsed_seconds)

        vehicle.update_battery(distance_km)
        vehicle.update_motor()
        vehicle.update_motor_temperature()
        vehicle.update_idle(elapsed_seconds)
        vehicle.update_speeding_status()

def generate_telemetry_events(
    fleet: list[VehicleState],
    elapsed_seconds: float = 1.0,
) -> list[dict]:
    """Advance the fleet and generate telemetry events."""

    simulate_tick(fleet, elapsed_seconds)

    timestamp = datetime.now(timezone.utc).isoformat()

    events = []

    for vehicle in fleet:
        event = vehicle.to_telemetry(
            event_id=str(uuid4()),
            timestamp=timestamp,
        )

        events.append(event)

    return events

def publish_telemetry(
    fleet: list[VehicleState],
    producer: VehicleTelemetryProducer,
    elapsed_seconds: float = 1.0,
) -> int:
    """Generate telemetry events and publish them to Kafka."""

    events = generate_telemetry_events(
        fleet,
        elapsed_seconds,
    )

    for event in events:
        producer.send(event)

    return len(events)