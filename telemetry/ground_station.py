from __future__ import annotations

from pathlib import Path
import json

import matplotlib.pyplot as plt


class GroundStationDashboard:
    def __init__(self, log_path: str):
        self.log_path = Path(log_path)

    def load_rows(self) -> list[dict]:
        rows: list[dict] = []
        if not self.log_path.exists():
            return rows

        with self.log_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    rows.append(json.loads(line))
        return rows

    def build_figure(self):
        rows = self.load_rows()
        if not rows:
            return None

        t = [row["t"] for row in rows]
        alt = [row["altitude_m"] for row in rows]
        vel = [row["velocity_mps"] for row in rows]
        anom = [row.get("anomaly_score", 0.0) for row in rows]

        fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
        axes[0].plot(t, alt, color="royalblue")
        axes[0].set_ylabel("Altitude (m)")
        axes[0].grid(True)

        axes[1].plot(t, vel, color="darkorange")
        axes[1].set_ylabel("Velocity (m/s)")
        axes[1].grid(True)

        axes[2].plot(t, anom, color="crimson")
        axes[2].set_ylabel("Anomaly Score")
        axes[2].set_xlabel("Time (s)")
        axes[2].grid(True)

        fig.suptitle("Mission Telemetry Dashboard")
        fig.tight_layout()
        return fig

    def plot(self) -> None:
        fig = self.build_figure()
        if fig is None:
            print("No telemetry rows found.")
            return
        plt.show()
