"""
collector.py
Captures RSSI signal data from a WiFi network interface.
Falls back to simulated data if the interface is unavailable.
"""

import time
import subprocess
import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SignalSample:
    timestamp: float
    rssi: float
    interface: str


@dataclass
class SignalData:
    samples: List[SignalSample] = field(default_factory=list)

    @property
    def timestamps(self) -> np.ndarray:
        return np.array([s.timestamp for s in self.samples])

    @property
    def rssi_values(self) -> np.ndarray:
        return np.array([s.rssi for s in self.samples])

    def __len__(self):
        return len(self.samples)


class RSSICollector:
    """
    Collects RSSI signal strength data from a WiFi interface.

    Parameters
    ----------
    interface : str
        WiFi interface name (e.g., 'wlan0').
    duration : float
        Collection duration in seconds.
    interval : float
        Sampling interval in seconds (default: 0.1s = 10 Hz).
    simulate : bool
        If True, generate synthetic data instead of reading hardware.
    """

    def __init__(
        self,
        interface: str = "wlan0",
        duration: float = 30.0,
        interval: float = 0.1,
        simulate: bool = False,
    ):
        self.interface = interface
        self.duration = duration
        self.interval = interval
        self.simulate = simulate

    def collect(self) -> SignalData:
        """Collect RSSI samples for the configured duration."""
        if self.simulate:
            return self._simulate()
        return self._collect_live()

    def _collect_live(self) -> SignalData:
        """Read RSSI from the OS (Linux iw/iwconfig)."""
        data = SignalData()
        end_time = time.time() + self.duration

        print(f"[RSSICollector] Collecting on {self.interface} for {self.duration}s ...")
        while time.time() < end_time:
            rssi = self._read_rssi()
            if rssi is not None:
                data.samples.append(
                    SignalSample(timestamp=time.time(), rssi=rssi, interface=self.interface)
                )
            time.sleep(self.interval)

        print(f"[RSSICollector] Collected {len(data)} samples.")
        return data

    def _read_rssi(self) -> Optional[float]:
        """Parse RSSI from `iw dev <iface> link` output."""
        try:
            result = subprocess.run(
                ["iw", "dev", self.interface, "link"],
                capture_output=True,
                text=True,
                timeout=1,
            )
            for line in result.stdout.splitlines():
                if "signal:" in line.lower():
                    # e.g. "signal: -65 dBm"
                    parts = line.strip().split()
                    idx = [p.lower() for p in parts].index("signal:")
                    return float(parts[idx + 1])
        except Exception:
            pass
        return None

    def _simulate(self) -> SignalData:
        """Generate synthetic RSSI data with injected motion events."""
        print(f"[RSSICollector] Simulating {self.duration}s of RSSI data ...")
        n = int(self.duration / self.interval)
        t = np.linspace(0, self.duration, n)

        # Baseline noise around -65 dBm
        base = -65.0
        noise = np.random.normal(0, 1.5, n)
        signal = base + noise

        # Inject two motion bursts
        for center in [self.duration * 0.3, self.duration * 0.7]:
            burst = np.exp(-0.5 * ((t - center) / 1.0) ** 2) * 10
            signal += burst

        data = SignalData()
        start = time.time()
        for i in range(n):
            data.samples.append(
                SignalSample(
                    timestamp=start + t[i],
                    rssi=float(signal[i]),
                    interface=self.interface,
                )
            )
        print(f"[RSSICollector] Simulated {len(data)} samples.")
        return data
