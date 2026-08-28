from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("EV-FleetIQ-SmokeTest")
        .master("local[*]")
        .getOrCreate()
    )

    print(f"Spark version: {spark.version}")

    data = [
        ("EV001", 85.5, 42.3),
        ("EV002", 72.1, 38.7),
        ("EV003", 91.4, 25.6),
    ]

    columns = ["vehicle_id", "battery_soc", "speed"]

    df = spark.createDataFrame(data, columns)

    df.show()

    spark.stop()


if __name__ == "__main__":
    main()