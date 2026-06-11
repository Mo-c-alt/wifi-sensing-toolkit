"""
utils.py
Helper utilities: save/load datasets, logging setup.
"""

import json
import csv
import logging
import numpy as np
from pathlib import Path
from typing import Union
from .collector import SignalData, SignalSample


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure and return the toolkit logger."""
    logger = logging.getLogger("wifi_sensing")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(name)s][%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def save_csv(data: SignalData, path: Union[str, Path]) -> None:
    """Save SignalData to a CSV file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "rssi", "interface"])
        for s in data.samples:
            writer.writerow([s.timestamp, s.rssi, s.interface])
    print(f"[utils] Saved {len(data)} samples → {path}")


def load_csv(path: Union[str, Path]) -> SignalData:
    """Load SignalData from a CSV file."""
    path = Path(path)
    data = SignalData()
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.samples.append(
                SignalSample(
                    timestamp=float(row["timestamp"]),
                    rssi=float(row["rssi"]),
                    interface=row["interface"],
                )
            )
    print(f"[utils] Loaded {len(data)} samples ← {path}")
    return data


def save_json(data: SignalData, path: Union[str, Path]) -> None:
    """Save SignalData to a JSON file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [
        {"timestamp": s.timestamp, "rssi": s.rssi, "interface": s.interface}
        for s in data.samples
    ]
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"[utils] Saved {len(data)} samples → {path}")


def load_json(path: Union[str, Path]) -> SignalData:
    """Load SignalData from a JSON file."""
    path = Path(path)
    with open(path, "r") as f:
        payload = json.load(f)
    data = SignalData()
    for item in payload:
        data.samples.append(
            SignalSample(
                timestamp=item["timestamp"],
                rssi=item["rssi"],
                interface=item["interface"],
            )
        )
    print(f"[utils] Loaded {len(data)} samples ← {path}")
    return data


def compute_variance(signal: np.ndarray, window: int = 10) -> np.ndarray:
    """Rolling variance over a 1D signal array."""
    variances = np.zeros(len(signal))
    for i in range(window, len(signal)):
        variances[i] = np.var(signal[i - window : i])
    return variances
