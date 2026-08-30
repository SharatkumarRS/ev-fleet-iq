import argparse
import time

from src.ingestion.kafka_producer import VehicleTelemetryProducer
from src.simulator.simulator import create_fleet, publish_telemetry
from src.utils.logger import get_logger


logger = get_logger("simulator")


def parse_args() -> argparse.Namespace:
    """Parse simulator command-line arguments."""

    parser = argparse.ArgumentParser(
        description="EV-FleetIQ telemetry simulator",
    )

    parser.add_argument(
        "--vehicles",
        type=int,
        default=10,
        help="Number of vehicles to simulate.",
    )

    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Seconds between simulation ticks.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.vehicles <= 0:
        raise ValueError("vehicles must be greater than zero")

    if args.interval <= 0:
        raise ValueError("interval must be greater than zero")

    fleet = create_fleet(args.vehicles)
    producer = VehicleTelemetryProducer()

    logger.info(
        "Starting EV telemetry simulator | vehicles=%s | interval=%ss",
        args.vehicles,
        args.interval,
    )

    try:
        while True:
            published_count = publish_telemetry(
                fleet,
                producer,
                elapsed_seconds=args.interval,
            )

            logger.info(
                "Simulation tick completed | events=%s",
                published_count,
            )

            time.sleep(args.interval)

    except KeyboardInterrupt:
        logger.info("Simulator stopped by user")

    finally:
        producer.close()


if __name__ == "__main__":
    main()