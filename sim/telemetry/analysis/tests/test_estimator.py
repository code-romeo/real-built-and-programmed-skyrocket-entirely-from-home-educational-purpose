from avionics.fusion import FlightStateEstimator, SensorSample
from analysis.anomaly_detection import AnomalyDetector
from sim.physics import RocketSimulation


def test_estimator_runs_and_outputs_state():
    estimator = FlightStateEstimator()
    sample = SensorSample(
        accel_x=0.0,
        accel_y=0.0,
        accel_z=9.80665,
        gyro_x=0.0,
        gyro_y=0.0,
        gyro_z=0.0,
        baro_altitude_m=0.0,
    )
    estimate = estimator.update(sample, 0.1)
    assert estimate.altitude_m >= 0.0
    assert -5.0 <= estimate.vertical_velocity_mps <= 5.0


def test_anomaly_detector_nominal_case():
    detector = AnomalyDetector()
    result = None
    for i in range(10):
        result = detector.evaluate(altitude_m=10 + i, velocity_mps=30, acceleration_mps2=5)
    assert result is not None
    assert result.score >= 0.0
    assert result.label in {"NOMINAL", "INSUFFICIENT_DATA", "ACCELERATION_OUTLIER", "VELOCITY_SPIKE", "UNSTABLE_DESCENT", "INVALID_ALTITUDE"}


def test_simulation_advances():
    sim = RocketSimulation()
    state1 = sim.step(0.1)
    state2 = sim.step(0.1)
    assert state2.t > state1.t
