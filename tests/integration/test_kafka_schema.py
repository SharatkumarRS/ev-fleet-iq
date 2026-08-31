import json
from pathlib import Path

from jsonschema import validate

from src.ingestion.kafka_producer import VehicleTelemetryProducer
from src.simulator.simulator import create_fleet, generate_telemetry_events


def test_simulator_event_matches_schema():
    fleet = create_fleet(1)

    events = generate_telemetry_events(
        fleet,
        elapsed_seconds=1.0,
    )

    event = events[0]

    schema_path = (
        Path(__file__).resolve().parents[2]
        / "schemas"
        / "telemetry"
        / "vehicle_telemetry_v1.json"
    )

    with schema_path.open(encoding="utf-8") as file:
        schema = json.load(file)

    validate(instance=event, schema=schema)
