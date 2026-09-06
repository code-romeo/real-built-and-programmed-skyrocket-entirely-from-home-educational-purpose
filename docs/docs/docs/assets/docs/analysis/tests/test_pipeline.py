from pathlib import Path

from analysis.mission_report import MissionReportGenerator
from telemetry.logger import TelemetryLogger
from telemetry.schema import TelemetryFrame


def test_mission_report_generator_reads_log(tmp_path: Path):
    log_path = tmp_path / "mission.jsonl"
    logger = TelemetryLogger(str(log_path))
    logger.append(
        TelemetryFrame(
            t=0.1,
            altitude_m=5.0,
            velocity_mps=10.0,
            acceleration_mps2=2.0,
            gyro_x_dps=0.0,
            gyro_y_dps=0.0,
            gyro_z_dps=0.0,
            accel_x_mps2=0.0,
            accel_y_mps2=0.0,
            accel_z_mps2=9.80665,
            baro_pa=101000.0,
            state="NOMINAL",
            anomaly_score=0.1,
        )
    )

    report = MissionReportGenerator(str(log_path)).generate()
    assert report.total_points == 1
    assert report.max_altitude_m == 5.0
