from __future__ import annotations

from dataclasses import dataclass
from random import Random

from avionics.fusion import SensorSample
from sim.physics import GRAVITY, RocketState


@dataclass
class SensorNoise:
    accel_sigma: float = 0.05
    gyro_sigma: float = 0.02
    altitude_sigma: float = 0.75
    gps_sigma: float = 1.5


class SensorSuite:
    """Generate simple simulated avionics measurements from a rocket state."""

    def __init__(self, noise: SensorNoise | None = None, seed: int | None = 0):
        self.noise = noise or SensorNoise()
        self._rng = Random(seed)

    def _normal(self, sigma: float) -> float:
        return 0.0 if sigma <= 0.0 else self._rng.gauss(0.0, sigma)

    def sample(self, state: RocketState) -> SensorSample:
        gps_altitude_m = None
        if state.t >= 2.0:
            gps_altitude_m = state.altitude_m + self._normal(self.noise.gps_sigma)

        return SensorSample(
            accel_x=self._normal(self.noise.accel_sigma),
            accel_y=self._normal(self.noise.accel_sigma),
            accel_z=state.acceleration_mps2 + GRAVITY + self._normal(self.noise.accel_sigma),
            gyro_x=self._normal(self.noise.gyro_sigma),
            gyro_y=self._normal(self.noise.gyro_sigma),
            gyro_z=self._normal(self.noise.gyro_sigma),
            baro_altitude_m=max(
                0.0,
                state.altitude_m + self._normal(self.noise.altitude_sigma),
            ),
            gps_altitude_m=gps_altitude_m,
        )
