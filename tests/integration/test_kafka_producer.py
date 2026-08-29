from src.ingestion.kafka_producer import VehicleTelemetryProducer


def test_kafka_producer_send():
    event = {
        "event_id": "evt_test_000001",
        "vehicle_id": "EV001",
        "driver_id": "DRV001",
        "timestamp": "2026-08-29T07:30:00Z"
    }

    producer = VehicleTelemetryProducer()

    try:
        producer.send(event)
    finally:
        producer.close()
