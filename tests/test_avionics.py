from avionics.estimator import FlightStateEstimator, SensorSample
from avionics.sensors import BarometerSensor, GPSSensor, IMUSensor


def test_sensor_fusion_produces_valid_estimate():
    estimator = FlightStateEstimator()
    sample = SensorSample(
        accel_x=0.0,
        accel_y=0.0,
        accel_z=9.80665,
        gyro_x=0.1,
        gyro_y=0.1,
        gyro_z=0.1,
        baro_altitude_m=120.0,
        gps_altitude_m=118.0,
    )
    estimate = estimator.update(sample, 0.1)
    assert estimate.altitude_m >= 0.0
    assert 0.0 <= estimate.confidence <= 1.0


def test_sensor_models_output_plausible_values():
    imu = IMUSensor(accel_noise_std=0.0, gyro_noise_std=0.0, seed=1)
    baro = BarometerSensor(altitude_noise_std=0.0, seed=1)
    gps = GPSSensor(altitude_noise_std=0.0, sample_period_s=0.5, seed=1)

    ax, ay, az, gx, gy, gz = imu.read(0.0, 0.0, 9.80665, 0.2, 0.1, 0.0)
    baro_alt = baro.read_altitude(50.0)
    gps_alt_1 = gps.read_altitude(50.0, t=0.0)
    gps_alt_2 = gps.read_altitude(50.0, t=0.1)

    assert (ax, ay, az) == (0.0, 0.0, 9.80665)
    assert (gx, gy, gz) == (0.2, 0.1, 0.0)
    assert baro_alt == 50.0
    assert gps_alt_1 == 50.0
    assert gps_alt_2 is None
