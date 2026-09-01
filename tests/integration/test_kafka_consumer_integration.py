import threading
import time

from src.ingestion.kafka_consumer import VehicleTelemetryConsumer
from src.ingestion.kafka_producer import VehicleTelemetryProducer


def test_kafka_consumer_receives_telemetry():
    group_id = "test-consumer-integration"

    consumer = VehicleTelemetryConsumer(
        topic="vehicle.telemetry",
        group_id=group_id,
    )

    producer = VehicleTelemetryProducer()

    received_event = []

    def consume_until_target():
        deadline = time.time() + 10

        for event in consumer.consume():
            if event["event_id"] == "integration-test-event":
                received_event.append(event)
                break

            if time.time() >= deadline:
                break

    consumer_thread = threading.Thread(
        target=consume_until_target,
        daemon=True,
    )

    try:
        consumer_thread.start()

        time.sleep(2)

        event = {
            "event_id": "integration-test-event",
            "vehicle_id": "EV999",
            "driver_id": "DRV999",
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

        producer.send(event)

        consumer_thread.join(timeout=10)

        assert len(received_event) == 1
        assert received_event[0]["event_id"] == "integration-test-event"
        assert received_event[0]["vehicle_id"] == "EV999"

    finally:
        producer.close()
        consumer.close()