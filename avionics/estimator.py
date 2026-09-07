from __future__ import annotations

from avionics.fusion import FlightStateEstimate, FlightStateEstimator
from avionics.sensors import SensorSuite
from sim.physics import RocketState


class EstimationPipeline:
    """Connect simulated sensors to the flight-state estimator."""

    def __init__(
        self,
        sensor_suite: SensorSuite | None = None,
        estimator: FlightStateEstimator | None = None,
    ):
        self.sensor_suite = sensor_suite or SensorSuite()
        self.estimator = estimator or FlightStateEstimator()

    def update_from_state(self, state: RocketState, dt: float) -> FlightStateEstimate:
        sample = self.sensor_suite.sample(state)
        return self.estimator.update(sample, dt)
