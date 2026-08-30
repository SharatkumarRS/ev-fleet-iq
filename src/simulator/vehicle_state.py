from dataclasses import dataclass
import math


BATTERY_CAPACITY_KWH = 60.0
ENERGY_CONSUMPTION_KWH_PER_100KM = 22.0
SPEED_LIMIT_KMH = 60.0



@dataclass
class VehicleState:
    """Current state of an EV in the simulator."""

    vehicle_id: str
    driver_id: str

    latitude: float
    longitude: float
    heading: float

    speed_kmh: float
    odometer_km: float

    battery_soc_pct: float
    battery_voltage_v: float
    battery_current_a: float
    battery_temperature_c: float

    motor_temperature_c: float
    motor_rpm: int
    brake_temperature_c: float

    harsh_acceleration: bool
    harsh_braking: bool
    speeding: bool
    idle_duration_sec: int

    order_id: str
    route_id: str
    delivery_status: str

    def update_position(self, elapsed_seconds: float) -> None:
        """Update GPS position and odometer based on speed and heading."""

        if elapsed_seconds <= 0 or self.speed_kmh <= 0:
            return

        distance_km = self.speed_kmh * elapsed_seconds / 3600

        heading_radians = math.radians(self.heading)

        latitude_delta = (
            distance_km * math.cos(heading_radians) / 111.0
        )

        longitude_delta = (
            distance_km
            * math.sin(heading_radians)
            / (111.0 * math.cos(math.radians(self.latitude)))
        )

        self.latitude += latitude_delta
        self.longitude += longitude_delta
        self.odometer_km += distance_km

    def update_battery(self, distance_km: float) -> None:
        """Reduce battery SOC based on distance travelled."""

        if distance_km <= 0 or self.battery_soc_pct <= 0:
            return

        energy_used_kwh = (
            distance_km * ENERGY_CONSUMPTION_KWH_PER_100KM / 100
        )

        soc_reduction_pct = (
            energy_used_kwh / BATTERY_CAPACITY_KWH * 100
        )

        self.battery_soc_pct = max(
            0.0,
            self.battery_soc_pct - soc_reduction_pct,
        )

    def update_motor(self) -> None:
        """Update motor RPM based on vehicle speed."""

        self.motor_rpm = round(self.speed_kmh * 80)

    def update_motor_temperature(self) -> None:
        """Update motor temperature based on vehicle speed."""

        if self.speed_kmh > 0:
            self.motor_temperature_c = min(
                120.0,
                self.motor_temperature_c + 0.5,
            )
        else:
            self.motor_temperature_c = max(
                25.0,
                self.motor_temperature_c - 0.3,
            )

    def apply_harsh_acceleration(self) -> None:
        """Apply a harsh acceleration event."""

        self.harsh_acceleration = True
        self.speed_kmh = min(120.0, self.speed_kmh + 15.0)

    def apply_harsh_braking(self) -> None:
        """Apply a harsh braking event."""

        self.harsh_braking = True
        self.speed_kmh = max(0.0, self.speed_kmh - 20.0)
        self.brake_temperature_c = min(
            500.0,
            self.brake_temperature_c + 8.0,
        )

    def update_speeding_status(self) -> None:
        """Update speeding status based on the configured speed limit."""

        self.speeding = self.speed_kmh > SPEED_LIMIT_KMH

    def update_idle(self, elapsed_seconds: float) -> None:
        """Track how long the vehicle has remained stationary."""

        if elapsed_seconds <= 0:
            return

        if self.speed_kmh == 0:
            self.idle_duration_sec += int(elapsed_seconds)
        else:
            self.idle_duration_sec = 0
            
    def to_telemetry(
        self,
        event_id: str,
        timestamp: str,
    ) -> dict:
        """Convert the current vehicle state to a telemetry event."""

        return {
            "event_id": event_id,
            "vehicle_id": self.vehicle_id,
            "driver_id": self.driver_id,
            "timestamp": timestamp,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "speed_kmh": self.speed_kmh,
            "odometer_km": self.odometer_km,
            "battery_soc_pct": self.battery_soc_pct,
            "battery_voltage_v": self.battery_voltage_v,
            "battery_current_a": self.battery_current_a,
            "battery_temperature_c": self.battery_temperature_c,
            "motor_temperature_c": self.motor_temperature_c,
            "motor_rpm": self.motor_rpm,
            "brake_temperature_c": self.brake_temperature_c,
            "harsh_acceleration": self.harsh_acceleration,
            "harsh_braking": self.harsh_braking,
            "speeding": self.speeding,
            "idle_duration_sec": self.idle_duration_sec,
            "order_id": self.order_id,
            "route_id": self.route_id,
            "delivery_status": self.delivery_status,
        }