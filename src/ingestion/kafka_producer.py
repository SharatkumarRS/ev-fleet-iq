import json
from kafka import KafkaProducer

from src.utils.logger import get_logger


logger = get_logger("kafka_producer")


class VehicleTelemetryProducer:
    """Kafka producer for EV vehicle telemetry events."""

    def __init__(
        self,
        bootstrap_servers: str = "localhost:9092",
        topic: str = "vehicle.telemetry",
    ):
        self.topic = topic

        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            key_serializer=lambda key: key.encode("utf-8"),
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        )

        logger.info(
            "Kafka producer connected to %s",
            bootstrap_servers,
        )

    def send(self, event: dict) -> None:
        """Publish a telemetry event to Kafka."""

        vehicle_id = event["vehicle_id"]

        self.producer.send(
            self.topic,
            key=vehicle_id,
            value=event,
        )

        logger.info(
            "Telemetry event published | vehicle_id=%s",
            vehicle_id,
        )

    def close(self) -> None:
        """Flush pending messages and close the producer."""

        self.producer.flush()
        self.producer.close()

        logger.info("Kafka producer closed")