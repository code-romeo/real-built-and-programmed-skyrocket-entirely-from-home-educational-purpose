from __future__ import annotations

from dataclasses import dataclass
from math import exp

GRAVITY = 9.80665
RHO0 = 1.225
SCALE_HEIGHT = 8500.0


@dataclass
class RocketParams:
    dry_mass_kg: float = 12.0
    propellant_mass_kg: float = 4.0
    reference_area_m2: float = 0.018
    drag_coefficient: float = 0.45
    thrust_newton: float = 650.0
    burn_time_s: float = 3.5


@dataclass
class RocketState:
    t: float
    altitude_m: float
    velocity_mps: float
    acceleration_mps2: float
    mass_kg: float
    thrust_newton: float
    drag_newton: float


class RocketSimulation:
    def __init__(self, params: RocketParams | None = None):
        self.params = params or RocketParams()
        self.reset()

    def reset(self) -> None:
        self.t = 0.0
        self.altitude_m = 0.0
        self.velocity_mps = 0.0
        self.acceleration_mps2 = 0.0
        self.mass_kg = self.params.dry_mass_kg + self.params.propellant_mass_kg

    def air_density(self, altitude_m: float) -> float:
        return RHO0 * exp(-max(altitude_m, 0.0) / SCALE_HEIGHT)

    def thrust_at_time(self, t: float) -> float:
        if t < 0.0 or t > self.params.burn_time_s:
            return 0.0
        return self.params.thrust_newton

    def mass_at_time(self, t: float) -> float:
        if t <= 0.0:
            return self.params.dry_mass_kg + self.params.propellant_mass_kg
        if t >= self.params.burn_time_s:
            return self.params.dry_mass_kg
        prop_remaining = self.params.propellant_mass_kg * (1.0 - t / self.params.burn_time_s)
        return self.params.dry_mass_kg + prop_remaining

    def step(self, dt: float) -> RocketState:
        self.t += dt
        thrust = self.thrust_at_time(self.t)
        self.mass_kg = self.mass_at_time(self.t)
        rho = self.air_density(self.altitude_m)
        drag = 0.5 * rho * self.velocity_mps**2 * self.params.drag_coefficient * self.params.reference_area_m2
        drag = drag if self.velocity_mps >= 0 else -drag
        net_force = thrust - drag - self.mass_kg * GRAVITY
        self.acceleration_mps2 = net_force / self.mass_kg
        self.velocity_mps += self.acceleration_mps2 * dt
        self.altitude_m = max(0.0, self.altitude_m + self.velocity_mps * dt)
        return RocketState(
            t=self.t,
            altitude_m=self.altitude_m,
            velocity_mps=self.velocity_mps,
            acceleration_mps2=self.acceleration_mps2,
            mass_kg=self.mass_kg,
            thrust_newton=thrust,
            drag_newton=abs(drag),
        )

    def run(self, duration_s: float, dt: float = 0.02) -> list[RocketState]:
        states: list[RocketState] = []
        steps = int(duration_s / dt)
        for _ in range(steps):
            states.append(self.step(dt))
        return states
