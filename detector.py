"""
detector.py
Motion and presence detection from processed WiFi signal data.
"""

import numpy as np
from dataclasses import dataclass
from typing import List
from .collector import SignalData
from .preprocessor import Preprocessor


@dataclass
class MotionEvent:
    start_time: float
    end_time: float
    peak_magnitude: float

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

    def __repr__(self):
        return (
            f"MotionEvent(start={self.start_time:.2f}s, "
            f"end={self.end_time:.2f}s, "
            f"duration={self.duration:.2f}s, "
            f"peak={self.peak_magnitude:.3f})"
        )


class MotionDetector:
    """
    Threshold-based motion detector.

    A motion event is declared when the absolute normalized signal
    exceeds `threshold` for at least `min_duration` seconds.

    Parameters
    ----------
    threshold : float
        Detection threshold on normalized signal (default: 1.5 σ).
    min_duration : float
        Minimum event duration in seconds (default: 0.5s).
    fs : float
        Sampling frequency in Hz (default: 10.0 Hz).
    preprocessor : Preprocessor, optional
        Custom preprocessor; a default one is created if None.
    """

    def __init__(
        self,
        threshold: float = 1.5,
        min_duration: float = 0.5,
        fs: float = 10.0,
        preprocessor: Preprocessor = None,
    ):
        self.threshold = threshold
        self.min_duration = min_duration
        self.fs = fs
        self.preprocessor = preprocessor or Preprocessor(fs=fs)

    def detect(self, data: SignalData) -> List[MotionEvent]:
        """
        Detect motion events in signal data.

        Returns
        -------
        List[MotionEvent]
        """
        timestamps, signal = self.preprocessor.process(data)
        above = np.abs(signal) > self.threshold

        events = []
        in_event = False
        start_idx = 0

        for i, active in enumerate(above):
            if active and not in_event:
                in_event = True
                start_idx = i
            elif not active and in_event:
                in_event = False
                duration = (i - start_idx) / self.fs
                if duration >= self.min_duration:
                    segment = signal[start_idx:i]
                    events.append(
                        MotionEvent(
                            start_time=float(timestamps[start_idx]),
                            end_time=float(timestamps[i - 1]),
                            peak_magnitude=float(np.abs(segment).max()),
                        )
                    )

        # Close open event at end of signal
        if in_event:
            duration = (len(signal) - start_idx) / self.fs
            if duration >= self.min_duration:
                segment = signal[start_idx:]
                events.append(
                    MotionEvent(
                        start_time=float(timestamps[start_idx]),
                        end_time=float(timestamps[-1]),
                        peak_magnitude=float(np.abs(segment).max()),
                    )
                )

        return events

    def is_occupied(self, data: SignalData) -> bool:
        """Return True if any motion was detected (simple occupancy check)."""
        return len(self.detect(data)) > 0
