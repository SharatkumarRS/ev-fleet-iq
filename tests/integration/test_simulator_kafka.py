from src.ingestion.kafka_producer import VehicleTelemetryProducer
from src.simulator.simulator import create_fleet, publish_telemetry


def test_simulator_publishes_to_kafka():
    fleet = create_fleet(2)

    for vehicle in fleet:
        vehicle.speed_kmh = 30.0

    producer = VehicleTelemetryProducer()

    try:
        published_count = publish_telemetry(
            fleet,
            producer,
            1.0,
        )

        assert published_count == 2
    finally:
        producer.close()
