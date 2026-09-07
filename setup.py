from pathlib import Path

from setuptools import find_packages, setup


def _read_requirements() -> list[str]:
    req_file = Path(__file__).parent / "requirements.txt"
    return [line.strip() for line in req_file.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")]


setup(
    name="autonomous-flight-intelligence-platform",
    version="0.1.0",
    description="Educational high-power rocketry simulation, avionics, telemetry, and analysis toolkit.",
    packages=find_packages(),
    install_requires=_read_requirements(),
)
