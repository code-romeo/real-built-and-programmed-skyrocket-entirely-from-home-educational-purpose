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
        with self.log_path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rows.append(json.loads(line))
        return rows

    def plot(self) -> None:
        rows = self.load_rows()
        if not rows:
            print("No telemetry rows found.")
            return

        t = [r["t"] for r in rows]
        alt = [r["altitude_m"] for r in rows]
        vel = [r["velocity_mps"] for r in rows]
        anom = [r.get("anomaly_score", 0.0) for r in rows]

        fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
        axs[0].plot(t, alt, color="royalblue")
        axs[0].set_ylabel("Altitude (m)")
        axs[0].grid(True)

        axs[1].plot(t, vel, color="darkorange")
        axs[1].set_ylabel("Velocity (m/s)")
        axs[1].grid(True)

        axs[2].plot(t, anom, color="crimson")
        axs[2].set_ylabel("Anomaly Score")
        axs[2].set_xlabel("Time (s)")
        axs[2].grid(True)

        fig.suptitle("Mission Telemetry Dashboard")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    GroundStationDashboard("logs/mission.jsonl").plot()
