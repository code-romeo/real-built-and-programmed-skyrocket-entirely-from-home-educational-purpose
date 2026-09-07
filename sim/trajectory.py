from __future__ import annotations

from dataclasses import dataclass

from sim.physics import RocketSimulation, RocketState


@dataclass
class TrajectoryMetrics:
    apogee_m: float
    time_to_apogee_s: float
    max_velocity_mps: float


class TrajectoryPredictor:
    def __init__(self, simulation: RocketSimulation | None = None):
        self.simulation = simulation or RocketSimulation()

    def simulate(self, duration_s: float, dt: float = 0.02) -> list[RocketState]:
        self.simulation.reset()
        return self.simulation.run(duration_s=duration_s, dt=dt)

    def summarize(self, states: list[RocketState]) -> TrajectoryMetrics:
        if not states:
            return TrajectoryMetrics(apogee_m=0.0, time_to_apogee_s=0.0, max_velocity_mps=0.0)

        apogee = max(s.altitude_m for s in states)
        max_velocity = max(s.velocity_mps for s in states)
        apogee_state = next((s for s in states if s.altitude_m >= apogee), states[-1])
        return TrajectoryMetrics(
            apogee_m=apogee,
            time_to_apogee_s=apogee_state.t,
            max_velocity_mps=max_velocity,
        )
