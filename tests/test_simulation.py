from sim.physics import RocketSimulation
from sim.trajectory import altitude_profile, summarize_trajectory


def test_simulation_generates_summary():
    states = RocketSimulation().run(duration_s=1.0, dt=0.1)

    summary = summarize_trajectory(states)

    assert states
    assert summary.apogee_m >= 0.0
    assert summary.max_velocity_mps > 0.0
    assert summary.flight_time_s == states[-1].t
    assert len(altitude_profile(states)) == len(states)
