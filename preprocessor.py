"""
preprocessor.py
Signal preprocessing: filtering, normalization, and segmentation.
"""

import numpy as np
from scipy.signal import butter, filtfilt
from typing import List, Tuple
from .collector import SignalData


class Preprocessor:
    """
    Preprocesses raw WiFi signal data.

    Parameters
    ----------
    lowpass_cutoff : float
        Low-pass filter cutoff frequency in Hz (default: 2.0 Hz).
    fs : float
        Sampling frequency in Hz (default: 10.0 Hz).
    window_size : int
        Sliding window size in samples (default: 50).
    step_size : int
        Step between windows in samples (default: 10).
    """

    def __init__(
        self,
        lowpass_cutoff: float = 2.0,
        fs: float = 10.0,
        window_size: int = 50,
        step_size: int = 10,
    ):
        self.lowpass_cutoff = lowpass_cutoff
        self.fs = fs
        self.window_size = window_size
        self.step_size = step_size
        self._b, self._a = self._design_filter()

    def _design_filter(self) -> Tuple[np.ndarray, np.ndarray]:
        nyq = self.fs / 2.0
        norm_cutoff = self.lowpass_cutoff / nyq
        norm_cutoff = min(norm_cutoff, 0.99)
        b, a = butter(4, norm_cutoff, btype="low")
        return b, a

    def filter(self, data: SignalData) -> np.ndarray:
        """Apply low-pass Butterworth filter to RSSI values."""
        rssi = data.rssi_values
        if len(rssi) < 15:
            return rssi
        return filtfilt(self._b, self._a, rssi)

    def normalize(self, signal: np.ndarray) -> np.ndarray:
        """Z-score normalization."""
        std = signal.std()
        if std == 0:
            return np.zeros_like(signal)
        return (signal - signal.mean()) / std

    def segment(self, signal: np.ndarray) -> List[np.ndarray]:
        """Slice signal into overlapping windows."""
        windows = []
        for start in range(0, len(signal) - self.window_size + 1, self.step_size):
            windows.append(signal[start : start + self.window_size])
        return windows

    def process(self, data: SignalData) -> Tuple[np.ndarray, np.ndarray]:
        """
        Full pipeline: filter → normalize.

        Returns
        -------
        timestamps : np.ndarray
        processed_signal : np.ndarray
        """
        filtered = self.filter(data)
        normalized = self.normalize(filtered)
        return data.timestamps, normalized
