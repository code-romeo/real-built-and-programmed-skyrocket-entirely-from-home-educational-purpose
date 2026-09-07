from __future__ import annotations

from pathlib import Path
import json

import matplotlib.pyplot as plt


def load_log(path: str) -> list[dict]:
    file_path = Path(path)
    rows: list[dict] = []
    if not file_path.exists():
        return rows

    with file_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def build_mission_figure(path: str = "logs/mission.jsonl"):
    rows = load_log(path)
    if not rows:
        return None

    t = [row["t"] for row in rows]
    alt = [row["altitude_m"] for row in rows]
    vel = [row["velocity_mps"] for row in rows]
    acc = [row["acceleration_mps2"] for row in rows]
    anom = [row.get("anomaly_score", 0.0) for row in rows]

    fig, axes = plt.subplots(4, 1, figsize=(11, 12), sharex=True)
    axes[0].plot(t, alt, color="royalblue")
    axes[0].set_ylabel("m")
    axes[0].grid(True)

    axes[1].plot(t, vel, color="darkorange")
    axes[1].set_ylabel("m/s")
    axes[1].grid(True)

    axes[2].plot(t, acc, color="seagreen")
    axes[2].set_ylabel("m/s²")
    axes[2].grid(True)

    axes[3].plot(t, anom, color="crimson")
    axes[3].set_ylabel("score")
    axes[3].set_xlabel("Time (s)")
    axes[3].grid(True)

    fig.suptitle("Educational Rocket Mission Analysis")
    fig.tight_layout()
    return fig


def plot_mission(path: str = "logs/mission.jsonl") -> None:
    fig = build_mission_figure(path)
    if fig is None:
        print("No mission data available.")
        return
    plt.show()
