from analysis.anomaly_detection import AnomalyDetector


def test_anomaly_detector_returns_nominal_after_warmup():
    detector = AnomalyDetector()

    result = None
    for i in range(10):
        result = detector.evaluate(
            altitude_m=10.0 + i,
            velocity_mps=30.0,
            acceleration_mps2=5.0,
        )

    assert result is not None
    assert result.label == "NOMINAL"


def test_anomaly_detector_flags_unstable_descent():
    detector = AnomalyDetector()
    for _ in range(5):
        detector.evaluate(altitude_m=150.0, velocity_mps=-5.0, acceleration_mps2=-3.0)

    result = detector.evaluate(
        altitude_m=150.0,
        velocity_mps=-31.0,
        acceleration_mps2=-4.0,
    )

    assert result.label == "UNSTABLE_DESCENT"
    assert result.score >= 0.95
