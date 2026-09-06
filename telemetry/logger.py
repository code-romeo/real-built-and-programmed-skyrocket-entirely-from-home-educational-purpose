from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import json

from telemetry.schema import TelemetryFrame, MissionSummary


@dataclass
class MissionRecord:
    frames: list[TelemetryFrame]
    summary: MissionSummary


class TelemetryLogger:
    def __init__(self, output_path: str = "mission_log.jsonl"):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, frame: TelemetryFrame) -> None:
        with self.output_path.open("a", encoding="utf-8") as f:
            f.write(frame.to_json() + "\n")

    def export_csv(self, csv_path: str) -> None:
        csv_file = Path(csv_path)
        rows = []
        with self.output_path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rows.append(json.loads(line))
        if not rows:
            return
        with csv_file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
