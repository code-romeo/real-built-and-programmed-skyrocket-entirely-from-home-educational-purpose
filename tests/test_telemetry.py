import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

from analysis.mission_report import MissionReportGenerator
from analysis.plots import build_mission_figure
from analysis.replay import MissionReplay
from telemetry.ground_station import GroundStationDashboard
from telemetry.logger import TelemetryLogger
from telemetry.schema import TelemetryFrame


def test_telemetry_pipeline_outputs_log_report_and_figures(tmp_path: Path):
    log_path = tmp_path / "mission.jsonl"
    csv_path = tmp_path / "mission.csv"
    report_path = tmp_path / "report.json"
    logger = TelemetryLogger(str(log_path))
    frame = TelemetryFrame(
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
        gps_alt_m=4.8,
        state="NOMINAL",
        anomaly_score=0.1,
    )

    logger.append(frame)
    logger.export_csv(str(csv_path))

    replay_points = MissionReplay(str(log_path)).load()
    dashboard_rows = GroundStationDashboard(str(log_path)).load_rows()
    reporter = MissionReportGenerator(str(log_path))
    report = reporter.generate()
    reporter.save_json(str(report_path))
    figure = build_mission_figure(str(log_path))

    assert replay_points[0].altitude_m == frame.altitude_m
    assert dashboard_rows[0]["state"] == "NOMINAL"
    assert report.total_points == 1
    assert figure is not None
    assert "altitude_m" in csv_path.read_text(encoding="utf-8")
    assert json.loads(report_path.read_text(encoding="utf-8"))["total_points"] == 1
