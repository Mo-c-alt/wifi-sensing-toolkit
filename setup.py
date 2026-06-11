from setuptools import setup, find_packages

setup(
    name="wifi-sensing-toolkit",
    version="0.1.0",
    description="A Python toolkit for WiFi-based motion and presence detection",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "matplotlib>=3.7.0",
    ],
)
