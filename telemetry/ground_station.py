from __future__ import annotations

from pathlib import Path
import json

from telemetry.schema import TelemetryFrame


class GroundStationReceiver:
    def __init__(self, log_path: str):
        self.log_path = Path(log_path)

    def decode_line(self, line: str) -> TelemetryFrame | None:
        if not line.strip():
            return None
        row = json.loads(line)
        return TelemetryFrame(**row)

    def load_frames(self) -> list[TelemetryFrame]:
        frames: list[TelemetryFrame] = []
        if not self.log_path.exists():
            return frames

        with self.log_path.open("r", encoding="utf-8") as stream:
            for line in stream:
                frame = self.decode_line(line)
                if frame is not None:
                    frames.append(frame)
        return frames

    def latest_frame(self) -> TelemetryFrame | None:
        frames = self.load_frames()
        return frames[-1] if frames else None
