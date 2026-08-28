# EV-FleetIQ

EV-FleetIQ is a real-world inspired data engineering platform for managing and analyzing an electric vehicle delivery fleet.

The project simulates a delivery company operating a fleet of electric vehicles equipped with GPS and OBD telemetry.

The platform is designed to process vehicle telemetry, delivery routes, vehicle health, and driver behavior using modern data engineering technologies.

## Business Scenario

A delivery company operates a fleet of electric vehicles.

Each vehicle continuously produces telemetry such as:

- GPS location
- Speed
- Battery state of charge
- Battery voltage
- Motor information
- Odometer
- Vehicle diagnostic information

Delivery routes are generated based on customer orders.

The platform will combine:

1. Delivery orders
2. Vehicle telemetry
3. Vehicle health information
4. Driver behavior
5. Route information

to provide operational and analytical insights.

## Project Goals

EV-FleetIQ will demonstrate a production-style data engineering pipeline capable of:

- Ingesting high-volume vehicle telemetry
- Processing real-time streaming data
- Validating incoming data
- Enriching telemetry with vehicle and order information
- Tracking vehicle health
- Analyzing driver behavior
- Monitoring battery performance
- Analyzing delivery routes
- Producing business-ready analytical datasets

## Target Architecture

The planned architecture is:

    EV / OBD Simulator
            |
            v
         Apache Kafka
            |
            v
    Spark Structured Streaming
            |
            v
       Bronze Layer
            |
            v
       Silver Layer
            |
            v
        Gold Layer
            |
            +-------------------+
            |                   |
            v                   v
      PostgreSQL          Analytics / BI

The complete architecture will be implemented incrementally during development.

## Technology Stack

### Current

- Python 3.11
- PySpark 4.2.0
- Java 17
- Apache Kafka
- PostgreSQL 17
- Docker Desktop
- Docker Compose
- pytest
- Git / GitHub

### Planned

- Kafka streaming
- Spark Structured Streaming
- Data quality validation
- Medallion architecture
- Vehicle telemetry simulator
- Route analytics
- Vehicle health analytics
- Driver behavior analytics
- Batch and streaming pipelines
- Analytical data models

## Repository Structure

    ev-fleet-iq/
    |
    +-- docker/
    |   +-- kafka/
    |   +-- postgres/
    |
    +-- src/
    |   +-- analytics/
    |   +-- ingestion/
    |   +-- quality/
    |   +-- simulator/
    |   +-- streaming/
    |   +-- transformation/
    |   +-- utils/
    |       +-- logger.py
    |
    +-- tests/
    |   +-- data_quality/
    |   +-- integration/
    |   +-- unit/
    |       +-- test_logger.py
    |       +-- test_smoke.py
    |
    +-- docker-compose.yml
    +-- requirements.txt
    +-- pytest.ini
    +-- README.md

## Current Infrastructure

### PostgreSQL

PostgreSQL runs locally through Docker.

Database:

    evfleet

Application user:

    evfleet_user

PostgreSQL is currently exposed on:

    localhost:5432

### Kafka

Kafka runs locally through Docker using KRaft mode.

The current telemetry topic is:

    vehicle.telemetry

The topic is configured with three partitions for local development.

Kafka is exposed on:

    localhost:9092

### PySpark

PySpark runs locally using:

    Python 3.11
    Java 17
    PySpark 4.2.0

Spark is currently configured to run in local mode.

## Testing

The project uses pytest.

Run the complete test suite:

    python -m pytest -v

Current tests cover:

- Basic EV-FleetIQ smoke validation
- Application logger creation
- Application logger output

## Logging

The project contains a reusable logging utility:

    src/utils/logger.py

Application components should use the project logger instead of relying on print statements for operational messages.

Example:

    from src.utils.logger import get_logger

    logger = get_logger("telemetry")

    logger.info("Processing vehicle EV001")

## Development Approach

The project is being developed incrementally using Agile-style tasks and sprints.

Each task should:

1. Have a clear objective
2. Be implemented in a small step
3. Be tested
4. Be committed independently where practical
5. Be pushed to GitHub
6. Leave the project in a working state

## Local Development

Activate the Python virtual environment:

    .\.venv\Scripts\Activate.ps1

Run tests:

    python -m pytest -v

Start infrastructure:

    docker compose up -d

Check running services:

    docker compose ps

Stop infrastructure:

    docker compose down

## Project Vision

The final EV-FleetIQ platform will simulate a realistic electric delivery fleet and demonstrate how a modern data engineering team can build a reliable streaming and analytics platform using open-source technologies.

The project intentionally runs locally so that the complete engineering workflow can be developed without requiring a paid cloud platform.

## Status

Sprint 0 - Development Environment and Infrastructure

Completed:

- Git repository
- Python environment
- Java environment
- Docker environment
- PostgreSQL
- Kafka
- PySpark
- pytest
- Application logging

Next:

- Complete Sprint 0 documentation
- Begin Sprint 1
- Build vehicle telemetry simulator
- Generate realistic EV telemetry
- Stream telemetry through Kafka
- Process telemetry using Spark Structured Streaming
