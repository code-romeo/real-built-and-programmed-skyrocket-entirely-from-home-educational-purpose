from __future__ import annotations

from pathlib import Path
import json
import matplotlib.pyplot as plt


def load_log(path: str) -> list[dict]:
    file_path = Path(path)
    rows: list[dict] = []
    if not file_path.exists():
        return rows
    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def plot_mission(path: str = "logs/mission.jsonl") -> None:
    rows = load_log(path)
    if not rows:
        print("No mission data available.")
        return

    t = [r["t"] for r in rows]
    alt = [r["altitude_m"] for r in rows]
    vel = [r["velocity_mps"] for r in rows]
    acc = [r["acceleration_mps2"] for r in rows]
    anom = [r.get("anomaly_score", 0.0) for r in rows]

    fig, axs = plt.subplots(4, 1, figsize=(11, 12), sharex=True)

    axs[0].plot(t, alt, label="Altitude", color="royalblue")
    axs[0].set_ylabel("m")
    axs[0].grid(True)

    axs[1].plot(t, vel, label="Velocity", color="darkorange")
    axs[1].set_ylabel("m/s")
    axs[1].grid(True)

    axs[2].plot(t, acc, label="Acceleration", color="seagreen")
    axs[2].set_ylabel("m/s²")
    axs[2].grid(True)

    axs[3].plot(t, anom, label="Anomaly", color="crimson")
    axs[3].set_ylabel("score")
    axs[3].set_xlabel("Time (s)")
    axs[3].grid(True)

    fig.suptitle("Educational Rocket Mission Analysis")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_mission()
