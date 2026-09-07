from analysis.anomaly_detection import AnomalyDetector
from analysis.replay import MissionReplay
from telemetry.ground_station import GroundStationReceiver
from telemetry.logger import TelemetryLogger
from telemetry.schema import TelemetryFrame


def _frame(t: float, altitude: float, velocity: float, acceleration: float, state: str = "NOMINAL") -> TelemetryFrame:
    return TelemetryFrame(
        t=t,
        altitude_m=altitude,
        velocity_mps=velocity,
        acceleration_mps2=acceleration,
        gyro_x_dps=0.0,
        gyro_y_dps=0.0,
        gyro_z_dps=0.0,
        accel_x_mps2=0.0,
        accel_y_mps2=0.0,
        accel_z_mps2=9.80665 + acceleration,
        baro_pa=101325.0,
        gps_lat=None,
        gps_lon=None,
        gps_alt_m=altitude,
        state=state,
        anomaly_score=0.0,
    )


def test_anomaly_detector_flags_unstable_descent():
    detector = AnomalyDetector(window_size=6)
    for _ in range(5):
        detector.evaluate(altitude_m=120.0, velocity_mps=-5.0, acceleration_mps2=0.0)
    result = detector.evaluate(altitude_m=120.0, velocity_mps=-35.0, acceleration_mps2=0.0)
    assert result.label == "UNSTABLE_DESCENT"


def test_telemetry_logger_ground_station_and_replay_round_trip(tmp_path):
    log_path = tmp_path / "mission.jsonl"
    logger = TelemetryLogger(str(log_path))
    logger.append(_frame(0.1, 10.0, 5.0, 1.0))
    logger.append(_frame(0.2, 20.0, 9.0, 1.2))

    receiver = GroundStationReceiver(str(log_path))
    frames = receiver.load_frames()
    assert len(frames) == 2
    assert receiver.latest_frame() is not None
    assert receiver.latest_frame().altitude_m == 20.0

    replay = MissionReplay(str(log_path))
    points = replay.load()
    assert len(points) == 2
    assert replay.max_altitude() == 20.0
