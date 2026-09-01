import json
from pathlib import Path

from jsonschema import ValidationError, validate
from kafka import KafkaConsumer


class VehicleTelemetryConsumer:
    """Kafka consumer for EV vehicle telemetry."""

    def __init__(
        self,
        bootstrap_servers: str = "localhost:9092",
        topic: str = "vehicle.telemetry",
        group_id: str = "ev-fleet-iq-consumer",
        validate_schema: bool = True,
    ) -> None:
        self.validate_schema = validate_schema
        self.schema = self._load_schema() if validate_schema else None

        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset="latest",
            enable_auto_commit=True,
            key_deserializer=lambda key: (
                key.decode("utf-8") if key else None
            ),
            value_deserializer=lambda value: json.loads(
                value.decode("utf-8")
            ),
        )

    @staticmethod
    def _load_schema() -> dict:
        """Load the vehicle telemetry JSON schema."""

        schema_path = (
            Path(__file__).resolve().parents[2]
            / "schemas"
            / "telemetry"
            / "vehicle_telemetry_v1.json"
        )

        with schema_path.open(encoding="utf-8") as file:
            return json.load(file)

    def consume(self):
        """Yield valid telemetry events from Kafka."""

        for message in self.consumer:
            event = message.value

            if self.validate_schema:
                try:
                    validate(
                        instance=event,
                        schema=self.schema,
                    )
                except ValidationError:
                    continue

            yield event

    def close(self) -> None:
        """Close the Kafka consumer."""

        self.consumer.close()