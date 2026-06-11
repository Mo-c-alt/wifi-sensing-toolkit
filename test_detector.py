"""
tests/test_detector.py
Unit tests for the MotionDetector.
"""

import pytest
import numpy as np
from wifi_sensing.collector import RSSICollector
from wifi_sensing.detector import MotionDetector


def make_data(duration=30.0, simulate=True):
    collector = RSSICollector(duration=duration, simulate=simulate)
    return collector.collect()


def test_simulated_data_has_samples():
    data = make_data()
    assert len(data) > 0


def test_detector_finds_events():
    data = make_data(duration=30.0)
    detector = MotionDetector(threshold=1.5)
    events = detector.detect(data)
    assert len(events) >= 1


def test_event_duration_positive():
    data = make_data()
    detector = MotionDetector(threshold=1.5)
    events = detector.detect(data)
    for event in events:
        assert event.duration > 0


def test_is_occupied_true():
    data = make_data()
    detector = MotionDetector(threshold=1.0)
    assert detector.is_occupied(data) is True


def test_high_threshold_no_events():
    data = make_data()
    detector = MotionDetector(threshold=100.0)
    events = detector.detect(data)
    assert len(events) == 0
