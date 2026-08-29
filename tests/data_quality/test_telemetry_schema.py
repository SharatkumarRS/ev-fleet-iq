import json
from pathlib import Path

import pytest
from jsonschema import ValidationError, validate


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SCHEMA_PATH = PROJECT_ROOT / "schemas" / "telemetry" / "vehicle_telemetry_v1.json"
VALID_EVENT_PATH = (
    PROJECT_ROOT
    / "schemas"
    / "telemetry"
    / "samples"
    / "valid_vehicle_telemetry.json"
)
INVALID_EVENT_PATH = (
    PROJECT_ROOT
    / "schemas"
    / "telemetry"
    / "samples"
    / "invalid_vehicle_telemetry.json"
)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def test_valid_vehicle_telemetry():
    schema = load_json(SCHEMA_PATH)
    event = load_json(VALID_EVENT_PATH)

    validate(instance=event, schema=schema)


def test_invalid_vehicle_telemetry_rejected():
    schema = load_json(SCHEMA_PATH)
    event = load_json(INVALID_EVENT_PATH)

    with pytest.raises(ValidationError):
        validate(instance=event, schema=schema)
