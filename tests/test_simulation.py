from sim.physics import RocketSimulation
from sim.trajectory import TrajectoryPredictor


def test_physics_simulation_advances():
    sim = RocketSimulation()
    state_1 = sim.step(0.1)
    state_2 = sim.step(0.1)
    assert state_2.t > state_1.t
    assert state_2.mass_kg <= state_1.mass_kg
    assert state_2.altitude_m >= 0.0


def test_trajectory_predictor_returns_metrics():
    predictor = TrajectoryPredictor()
    states = predictor.simulate(duration_s=5.0, dt=0.05)
    metrics = predictor.summarize(states)
    assert states
    assert metrics.apogee_m >= 0.0
    assert metrics.time_to_apogee_s >= 0.0
