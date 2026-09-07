from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from sim.physics import RocketState


@dataclass
class TrajectorySummary:
    apogee_m: float
    max_velocity_mps: float
    max_acceleration_mps2: float
    flight_time_s: float


def summarize_trajectory(states: Sequence[RocketState]) -> TrajectorySummary:
    """Summarize a simulated trajectory for analysis and reporting."""
    if not states:
        return TrajectorySummary(
            apogee_m=0.0,
            max_velocity_mps=0.0,
            max_acceleration_mps2=0.0,
            flight_time_s=0.0,
        )

    return TrajectorySummary(
        apogee_m=max(state.altitude_m for state in states),
        max_velocity_mps=max(abs(state.velocity_mps) for state in states),
        max_acceleration_mps2=max(abs(state.acceleration_mps2) for state in states),
        flight_time_s=states[-1].t,
    )


def altitude_profile(states: Sequence[RocketState]) -> list[tuple[float, float]]:
    """Return time/altitude pairs for plotting or validation."""
    return [(state.t, state.altitude_m) for state in states]
