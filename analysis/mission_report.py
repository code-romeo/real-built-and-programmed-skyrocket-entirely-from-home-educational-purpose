from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json

from analysis.plots import load_log
from analysis.replay import MissionReplay
from telemetry.schema import MissionSummary


@dataclass
class Report:
    mission_name: str
    summary: MissionSummary
    max_altitude_m: float
    total_points: int


class MissionReportGenerator:
    def __init__(self, log_path: str):
        self.log_path = Path(log_path)

    def generate(self, mission_name: str = "Educational Flight Mission") -> Report:
        points = MissionReplay(str(self.log_path)).load()
        rows = load_log(str(self.log_path))
        max_altitude = max((point.altitude_m for point in points), default=0.0)
        max_velocity = max((abs(point.velocity_mps) for point in points), default=0.0)
        max_accel = max((abs(row["acceleration_mps2"]) for row in rows), default=0.0)
        anomaly_events = sum(1 for point in points if point.anomaly_score >= 0.5)

        summary = MissionSummary(
            max_altitude_m=max_altitude,
            max_velocity_mps=max_velocity,
            max_acceleration_mps2=max_accel,
            burn_time_s=0.0,
            anomaly_events=anomaly_events,
            landing_time_s=points[-1].t if points else None,
        )
        return Report(
            mission_name=mission_name,
            summary=summary,
            max_altitude_m=max_altitude,
            total_points=len(points),
        )

    def save_json(
        self,
        output_path: str,
        mission_name: str = "Educational Flight Mission",
    ) -> None:
        report = self.generate(mission_name=mission_name)
        payload = {
            "mission_name": report.mission_name,
            "summary": asdict(report.summary),
            "max_altitude_m": report.max_altitude_m,
            "total_points": report.total_points,
        }
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
