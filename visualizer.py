"""
visualizer.py
Plotting utilities for WiFi signal data and detected events.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import List, Optional
from .collector import SignalData
from .detector import MotionEvent
from .preprocessor import Preprocessor


def plot_signal(
    data: SignalData,
    events: Optional[List[MotionEvent]] = None,
    title: str = "WiFi Signal Strength Over Time",
    save_path: Optional[str] = None,
    show: bool = True,
) -> plt.Figure:
    """
    Plot raw RSSI signal with optional motion event overlays.

    Parameters
    ----------
    data : SignalData
        Collected signal samples.
    events : list of MotionEvent, optional
        Detected motion events to highlight.
    title : str
        Plot title.
    save_path : str, optional
        File path to save the figure (e.g., 'output.png').
    show : bool
        Whether to call plt.show().

    Returns
    -------
    matplotlib.figure.Figure
    """
    preprocessor = Preprocessor()
    timestamps, processed = preprocessor.process(data)
    t_rel = timestamps - timestamps[0]  # relative time in seconds

    fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
    fig.suptitle(title, fontsize=14, fontweight="bold")

    # --- Top: Raw RSSI ---
    ax1 = axes[0]
    ax1.plot(t_rel, data.rssi_values, color="#3a86ff", linewidth=0.8, alpha=0.9, label="Raw RSSI")
    ax1.set_ylabel("RSSI (dBm)")
    ax1.set_title("Raw Signal")
    ax1.grid(True, linestyle="--", alpha=0.4)
    ax1.legend(loc="upper right", fontsize=9)

    # --- Bottom: Processed (normalized) ---
    ax2 = axes[1]
    ax2.plot(t_rel, processed, color="#8338ec", linewidth=0.9, alpha=0.9, label="Processed (norm.)")
    ax2.axhline(0, color="gray", linewidth=0.5, linestyle="--")
    ax2.set_ylabel("Normalized Amplitude")
    ax2.set_xlabel("Time (s)")
    ax2.set_title("Processed Signal")
    ax2.grid(True, linestyle="--", alpha=0.4)

    # Overlay motion events
    if events:
        for event in events:
            t_start = event.start_time - timestamps[0]
            t_end = event.end_time - timestamps[0]
            for ax in axes:
                ax.axvspan(t_start, t_end, alpha=0.2, color="#ff006e", zorder=0)

        motion_patch = mpatches.Patch(color="#ff006e", alpha=0.4, label="Motion Event")
        ax2.legend(handles=[
            mpatches.Patch(color="#8338ec", label="Processed (norm.)"),
            motion_patch,
        ], loc="upper right", fontsize=9)

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"[Visualizer] Saved to {save_path}")

    if show:
        plt.show()

    return fig


def plot_events_summary(events: List[MotionEvent], show: bool = True) -> plt.Figure:
    """Bar chart of motion event durations."""
    if not events:
        print("[Visualizer] No events to plot.")
        return None

    labels = [f"Event {i+1}" for i in range(len(events))]
    durations = [e.duration for e in events]
    peaks = [e.peak_magnitude for e in events]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    fig.suptitle("Motion Events Summary", fontsize=13, fontweight="bold")

    ax1.bar(labels, durations, color="#3a86ff", edgecolor="white")
    ax1.set_title("Duration (s)")
    ax1.set_ylabel("Seconds")

    ax2.bar(labels, peaks, color="#ff006e", edgecolor="white")
    ax2.set_title("Peak Magnitude (σ)")
    ax2.set_ylabel("Normalized amplitude")

    plt.tight_layout()
    if show:
        plt.show()
    return fig
