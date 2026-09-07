from __future__ import annotations

from pathlib import Path
import json


def load_mission_rows(path: str) -> list[dict]:
    file_path = Path(path)
    rows: list[dict] = []
    if not file_path.exists():
        return rows
    with file_path.open("r", encoding="utf-8") as stream:
        for line in stream:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def plot_mission(path: str) -> None:
    rows = load_mission_rows(path)
    if not rows:
        return

    import matplotlib.pyplot as plt

    t = [r["t"] for r in rows]
    alt = [r["altitude_m"] for r in rows]
    vel = [r["velocity_mps"] for r in rows]
    acc = [r["acceleration_mps2"] for r in rows]

    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    axes[0].plot(t, alt)
    axes[0].set_ylabel("Altitude (m)")
    axes[1].plot(t, vel)
    axes[1].set_ylabel("Velocity (m/s)")
    axes[2].plot(t, acc)
    axes[2].set_ylabel("Acceleration (m/s²)")
    axes[2].set_xlabel("Time (s)")
    for axis in axes:
        axis.grid(True)
    fig.tight_layout()
    plt.show()
