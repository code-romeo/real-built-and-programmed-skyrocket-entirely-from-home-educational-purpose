from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class ReplayPoint:
    t: float
    altitude_m: float
    velocity_mps: float
    anomaly_score: float
    state: str


class MissionReplay:
    def __init__(self, log_path: str):
        self.log_path = Path(log_path)

    def load(self) -> list[ReplayPoint]:
        points: list[ReplayPoint] = []
        if not self.log_path.exists():
            return points
        with self.log_path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                row = json.loads(line)
                points.append(
                    ReplayPoint(
                        t=float(row["t"]),
                        altitude_m=float(row["altitude_m"]),
                        velocity_mps=float(row["velocity_mps"]),
                        anomaly_score=float(row.get("anomaly_score", 0.0)),
                        state=str(row.get("state", "UNKNOWN")),
                    )
                )
        return points

    def max_altitude(self) -> float:
        return max((p.altitude_m for p in self.load()), default=0.0)
