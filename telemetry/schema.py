from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
import json


@dataclass
class TelemetryFrame:
    t: float
    altitude_m: float
    velocity_mps: float
    acceleration_mps2: float
    gyro_x_dps: float
    gyro_y_dps: float
    gyro_z_dps: float
    accel_x_mps2: float
    accel_y_mps2: float
    accel_z_mps2: float
    baro_pa: float
    gps_lat: float | None = None
    gps_lon: float | None = None
    gps_alt_m: float | None = None
    state: str = "UNKNOWN"
    anomaly_score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), separators=(",", ":"), sort_keys=True)


@dataclass
class MissionSummary:
    max_altitude_m: float
    max_velocity_mps: float
    max_acceleration_mps2: float
    burn_time_s: float
    anomaly_events: int
    landing_time_s: float | None = None
