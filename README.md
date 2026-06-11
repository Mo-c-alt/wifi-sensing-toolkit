# 📡 wifi-sensing-toolkit

A Python toolkit for WiFi sensing — detect motion, presence, and activity using WiFi signals without cameras or wearables.

---

## 🔍 What is WiFi Sensing?

WiFi sensing (also called WiFi-based passive radar) uses variations in WiFi signal properties — such as **Channel State Information (CSI)** or **Received Signal Strength Indicator (RSSI)** — to detect physical changes in the environment. When a person moves, it disturbs the wireless signals between a router and a device, and those disturbances can be analyzed to infer:

- 🚶 Presence / occupancy detection
- 🤸 Motion and gesture recognition
- 💤 Breathing and sleep monitoring
- 🏠 Room-level localization

---

## ✨ Features

- 📥 **Data collection** — Capture RSSI / CSI data from WiFi interfaces
- 🔧 **Preprocessing** — Filter, normalize, and segment signal data
- 📊 **Visualization** — Plot signal over time with annotated events
- 🤖 **Detection models** — Threshold-based and ML-based motion detection
- 📁 **Dataset utilities** — Save, load, and label datasets for training

---

## 📦 Requirements

- Python 3.8+
- Linux (for CSI capture support) or any OS for RSSI-based sensing
- See `requirements.txt` for full dependencies

---

## 🚀 Installation

```bash
git clone https://github.com/YOUR_USERNAME/wifi-sensing-toolkit.git
cd wifi-sensing-toolkit
pip install -r requirements.txt
```

---

## 🗂️ Project Structure

```
wifi-sensing-toolkit/
├── data/                  # Raw and processed signal data
├── notebooks/             # Jupyter notebooks for exploration
├── wifi_sensing/
│   ├── __init__.py
│   ├── collector.py       # Signal data collection
│   ├── preprocessor.py    # Filtering and normalization
│   ├── detector.py        # Motion/presence detection
│   ├── visualizer.py      # Plotting utilities
│   └── utils.py           # Helper functions
├── tests/                 # Unit tests
├── requirements.txt
├── setup.py
└── README.md
```

---

## ⚡ Quick Start

```python
from wifi_sensing.collector import RSSICollector
from wifi_sensing.detector import MotionDetector
from wifi_sensing.visualizer import plot_signal

# Collect signal data
collector = RSSICollector(interface="wlan0", duration=30)
data = collector.collect()

# Detect motion
detector = MotionDetector(threshold=5.0)
events = detector.detect(data)

# Visualize
plot_signal(data, events=events)
```

---

## 📖 Modules

### `collector.py`
Captures RSSI or CSI data from a WiFi network interface.

### `preprocessor.py`
Applies low-pass filtering, normalization, and sliding window segmentation to raw signal data.

### `detector.py`
Implements threshold-based and machine-learning-based detection of motion and presence.

### `visualizer.py`
Generates time-series plots of signal strength with event annotations.

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push and open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

Inspired by research in passive WiFi radar, CSI-based sensing, and device-free localization.

