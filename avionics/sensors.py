from __future__ import annotations

from dataclasses import dataclass
from random import Random


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


class IMUSensor:
    def __init__(self, accel_noise_std: float = 0.05, gyro_noise_std: float = 0.02, seed: int | None = None):
        self.accel_noise_std = accel_noise_std
        self.gyro_noise_std = gyro_noise_std
        self._rng = Random(seed)

    def read(
        self,
        accel_x: float,
        accel_y: float,
        accel_z: float,
        gyro_x: float,
        gyro_y: float,
        gyro_z: float,
    ) -> tuple[float, float, float, float, float, float]:
        return (
            accel_x + self._rng.gauss(0.0, self.accel_noise_std),
            accel_y + self._rng.gauss(0.0, self.accel_noise_std),
            accel_z + self._rng.gauss(0.0, self.accel_noise_std),
            gyro_x + self._rng.gauss(0.0, self.gyro_noise_std),
            gyro_y + self._rng.gauss(0.0, self.gyro_noise_std),
            gyro_z + self._rng.gauss(0.0, self.gyro_noise_std),
        )


class BarometerSensor:
    def __init__(self, altitude_noise_std: float = 0.7, seed: int | None = None):
        self.altitude_noise_std = altitude_noise_std
        self._rng = Random(seed)

    def read_altitude(self, true_altitude_m: float) -> float:
        return max(0.0, true_altitude_m + self._rng.gauss(0.0, self.altitude_noise_std))


class GPSSensor:
    def __init__(self, altitude_noise_std: float = 1.5, sample_period_s: float = 0.2, seed: int | None = None):
        self.altitude_noise_std = altitude_noise_std
        self.sample_period_s = sample_period_s
        self._last_sample_time = -sample_period_s
        self._rng = Random(seed)

    def read_altitude(self, true_altitude_m: float, t: float) -> float | None:
        if t - self._last_sample_time < self.sample_period_s:
            return None
        self._last_sample_time = t
        return max(0.0, true_altitude_m + self._rng.gauss(0.0, self.altitude_noise_std))
