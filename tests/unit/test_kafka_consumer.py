from unittest.mock import MagicMock, patch

from src.ingestion.kafka_consumer import VehicleTelemetryConsumer


VALID_EVENT = {
    "event_id": "evt-001",
    "vehicle_id": "EV001",
    "driver_id": "DRV001",
    "timestamp": "2026-09-01T12:00:00Z",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "speed_kmh": 30.0,
    "odometer_km": 10000.0,
    "battery_soc_pct": 80.0,
    "battery_voltage_v": 400.0,
    "battery_current_a": 0.0,
    "battery_temperature_c": 30.0,
    "motor_temperature_c": 35.0,
    "motor_rpm": 2400,
    "brake_temperature_c": 30.0,
    "harsh_acceleration": False,
    "harsh_braking": False,
    "speeding": False,
    "idle_duration_sec": 0,
    "order_id": "ORD999999",
    "route_id": "RT99999",
    "delivery_status": "ASSIGNED",
}


@patch("src.ingestion.kafka_consumer.KafkaConsumer")
def test_consumer_initialization(mock_kafka_consumer):
    consumer = VehicleTelemetryConsumer(
        bootstrap_servers="localhost:9092",
        topic="vehicle.telemetry",
        group_id="test-consumer",
    )

    mock_kafka_consumer.assert_called_once()

    args, kwargs = mock_kafka_consumer.call_args

    assert args[0] == "vehicle.telemetry"
    assert kwargs["bootstrap_servers"] == "localhost:9092"
    assert kwargs["group_id"] == "test-consumer"
    assert kwargs["auto_offset_reset"] == "latest"

    consumer.close()


@patch("src.ingestion.kafka_consumer.KafkaConsumer")
def test_consumer_yields_valid_events(mock_kafka_consumer):
    mock_message = MagicMock()
    mock_message.value = VALID_EVENT

    mock_kafka_consumer.return_value.__iter__.return_value = [
        mock_message,
    ]

    consumer = VehicleTelemetryConsumer()

    events = list(consumer.consume())

    assert events == [VALID_EVENT]

    consumer.close()


@patch("src.ingestion.kafka_consumer.KafkaConsumer")
def test_consumer_rejects_invalid_event(mock_kafka_consumer):
    invalid_event = {
        "event_id": "evt-invalid",
        "vehicle_id": "EV001",
    }

    mock_message = MagicMock()
    mock_message.value = invalid_event

    mock_kafka_consumer.return_value.__iter__.return_value = [
        mock_message,
    ]

    consumer = VehicleTelemetryConsumer()

    events = list(consumer.consume())

    assert events == []

    consumer.close()
