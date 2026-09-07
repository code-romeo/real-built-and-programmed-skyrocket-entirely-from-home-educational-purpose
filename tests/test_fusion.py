from avionics.estimator import EstimationPipeline
from avionics.fusion import FlightStateEstimator, SensorSample
from avionics.sensors import SensorNoise, SensorSuite
from sim.physics import RocketSimulation


def test_estimator_updates_with_sensor_sample():
    estimator = FlightStateEstimator()
    sample = SensorSample(
        accel_x=0.0,
        accel_y=0.0,
        accel_z=9.80665,
        gyro_x=0.0,
        gyro_y=0.0,
        gyro_z=0.0,
        baro_altitude_m=5.0,
    )

    estimate = estimator.update(sample, 0.1)

    assert estimate.altitude_m >= 0.0
    assert estimate.confidence >= 0.0


def test_pipeline_samples_simulated_state():
    sim = RocketSimulation()
    state = sim.step(0.1)
    pipeline = EstimationPipeline(
        sensor_suite=SensorSuite(noise=SensorNoise(), seed=1),
    )

    estimate = pipeline.update_from_state(state, 0.1)

    assert estimate.altitude_m >= 0.0
    assert estimate.vertical_acceleration_mps2 == estimate.vertical_acceleration_mps2
