from __future__ import annotations

from sim.physics import RocketSimulation
from avionics.estimator import FlightStateEstimator
from avionics.sensors import SensorSample
from analysis.anomaly_detection import AnomalyDetector
from telemetry.schema import TelemetryFrame
from telemetry.logger import TelemetryLogger


def run_demo(duration_s: float = 20.0, dt: float = 0.05) -> None:
    sim = RocketSimulation()
    estimator = FlightStateEstimator()
    detector = AnomalyDetector()
    logger = TelemetryLogger("logs/mission.jsonl")

    steps = int(duration_s / dt)
    for _ in range(steps):
        state = sim.step(dt)
        sample = SensorSample(
            accel_x=0.02,
            accel_y=-0.01,
            accel_z=state.acceleration_mps2 + 9.80665,
            gyro_x=0.2,
            gyro_y=0.1,
            gyro_z=0.05,
            baro_altitude_m=state.altitude_m,
            gps_altitude_m=state.altitude_m if state.t > 2 else None,
        )
        estimate = estimator.update(sample, dt)
        anomaly = detector.evaluate(
            altitude_m=estimate.altitude_m,
            velocity_mps=estimate.vertical_velocity_mps,
            acceleration_mps2=estimate.vertical_acceleration_mps2,
        )
        frame = TelemetryFrame(
            t=state.t,
            altitude_m=estimate.altitude_m,
            velocity_mps=estimate.vertical_velocity_mps,
            acceleration_mps2=estimate.vertical_acceleration_mps2,
            gyro_x_dps=sample.gyro_x,
            gyro_y_dps=sample.gyro_y,
            gyro_z_dps=sample.gyro_z,
            accel_x_mps2=sample.accel_x,
            accel_y_mps2=sample.accel_y,
            accel_z_mps2=sample.accel_z,
            baro_pa=max(500.0, 101325.0 * (1.0 - estimate.altitude_m / 44330.0) ** 5.255),
            gps_lat=40.0,
            gps_lon=-73.0,
            gps_alt_m=sample.gps_altitude_m,
            state=anomaly.label,
            anomaly_score=anomaly.score,
        )
        logger.append(frame)
        print(
            f"t={frame.t:5.2f}s alt={frame.altitude_m:8.2f}m vel={frame.velocity_mps:7.2f}m/s "
            f"anom={frame.state:<20} score={frame.anomaly_score:.2f}"
        )


if __name__ == "__main__":
    run_demo()
