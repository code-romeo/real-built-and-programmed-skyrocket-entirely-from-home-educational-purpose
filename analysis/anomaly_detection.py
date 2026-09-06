from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev


@dataclass
class AnomalyResult:
    score: float
    label: str
    reason: str


class AnomalyDetector:
    def __init__(self, window_size: int = 20):
        self.window_size = window_size
        self.altitude_window: list[float] = []
        self.velocity_window: list[float] = []
        self.accel_window: list[float] = []

    def _push(self, window: list[float], value: float) -> None:
        window.append(value)
        if len(window) > self.window_size:
            window.pop(0)

    def evaluate(self, altitude_m: float, velocity_mps: float, acceleration_mps2: float) -> AnomalyResult:
        self._push(self.altitude_window, altitude_m)
        self._push(self.velocity_window, velocity_mps)
        self._push(self.accel_window, acceleration_mps2)

        if len(self.accel_window) < 5:
            return AnomalyResult(score=0.0, label="INSUFFICIENT_DATA", reason="Not enough samples yet")

        accel_mu = mean(self.accel_window)
        accel_sigma = pstdev(self.accel_window) or 1e-6
        z_accel = abs(acceleration_mps2 - accel_mu) / accel_sigma

        if velocity_mps < -30 and altitude_m > 100:
            return AnomalyResult(score=0.95, label="UNSTABLE_DESCENT", reason="High descent rate above ground")
        if z_accel > 3.0:
            return AnomalyResult(score=min(1.0, z_accel / 6.0), label="ACCELERATION_OUTLIER", reason="Acceleration deviates sharply from expected window")
        if altitude_m < 0:
            return AnomalyResult(score=0.9, label="INVALID_ALTITUDE", reason="Altitude below zero")
        if velocity_mps > 400:
            return AnomalyResult(score=0.8, label="VELOCITY_SPIKE", reason="Velocity exceeds expected profile")

        return AnomalyResult(score=0.05, label="NOMINAL", reason="Within expected flight envelope")
