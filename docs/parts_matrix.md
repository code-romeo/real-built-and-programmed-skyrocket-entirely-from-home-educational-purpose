# Safe Parts Matrix

This matrix is intended to help organize an **educational aerospace software project** around safe, legal components.

| Category | Example Type | Purpose | Notes |
|---|---|---|---|
| Microcontroller | STM32 / Arduino-class board | Flight logic and data handling | Use vendor documentation |
| IMU | 9-axis sensor module | Orientation and acceleration sensing | Calibration required |
| Barometer | Pressure sensor module | Altitude estimation | Use environmental shielding if needed |
| GPS | Receiver module | Position tracking | Outdoor use only |
| Storage | microSD module | Telemetry logging | Verify write reliability |
| Radio | Legal low-power telemetry module | Ground communication | Follow local RF regulations |
| Power | Regulated battery pack | Clean power supply | Add voltage monitoring |
| Display | Small OLED / LCD | Status readout | Optional |
| Enclosure | Project box / payload bay mockup | Organize hardware | Keep modular |

## Software mapping

- `sim/physics.py` → expected flight motion
- `avionics/fusion.py` → state estimation from sensors
- `analysis/anomaly_detection.py` → health monitoring
- `telemetry/logger.py` → structured mission logging
- `analysis/replay.py` → post-flight review

## Safety reminder

This repository is for educational and lawful research-oriented work only.
