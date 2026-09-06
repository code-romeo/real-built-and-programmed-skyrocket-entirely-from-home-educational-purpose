from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass
class SensorSample:
    accel_x: float
    accel_y: float
    accel_z: float
    gyro_x: float
    gyro_y: float
    gyro_z: float
    baro_altitude_m: float
    gps_altitude_m: float | None = None


@dataclass
class FlightStateEstimate:
    altitude_m: float
    vertical_velocity_mps: float
    vertical_acceleration_mps2: float
    pitch_deg: float
    roll_deg: float
    yaw_deg: float
    confidence: float


class FlightStateEstimator:
    def __init__(self):
        self._altitude_m = 0.0
        self._velocity_mps = 0.0
        self._last_accel_z = 0.0

    def update(self, sample: SensorSample, dt: float) -> FlightStateEstimate:
        accel_mag = sqrt(sample.accel_x**2 + sample.accel_y**2 + sample.accel_z**2)
        vertical_accel = sample.accel_z - 9.80665
        self._velocity_mps += vertical_accel * dt
        self._altitude_m = max(0.0, self._altitude_m + self._velocity_mps * dt)

        baro_weight = 0.65
        gps_weight = 0.25 if sample.gps_altitude_m is not None else 0.0
        inertial_weight = 0.10

        fused_altitude = self._altitude_m * inertial_weight + sample.baro_altitude_m * baro_weight
        if sample.gps_altitude_m is not None:
            fused_altitude += sample.gps_altitude_m * gps_weight

        confidence = min(1.0, max(0.0, 1.0 - abs(accel_mag - 9.80665) / 20.0))
        self._last_accel_z = sample.accel_z

        return FlightStateEstimate(
            altitude_m=max(0.0, fused_altitude),
            vertical_velocity_mps=self._velocity_mps,
            vertical_acceleration_mps2=vertical_accel,
            pitch_deg=sample.gyro_x * 0.02,
            roll_deg=sample.gyro_y * 0.02,
            yaw_deg=sample.gyro_z * 0.02,
            confidence=confidence,
        )
