import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = Path(os.environ.get("ECHO_DATA", r"C:\ECHO_DATA"))

CONSENT_DIR = DATA_ROOT / "consent"
RAW_DIR = DATA_ROOT / "raw"
WAV16K_DIR = DATA_ROOT / "wav16k"
CLIPS_DIR = DATA_ROOT / "clips"
EMOTION_DIR = DATA_ROOT / "emotion"
MANIFEST_DIR = DATA_ROOT / "manifests"

CONFIG_DIR = REPO_ROOT / "configs"
LOG_DIR = REPO_ROOT / "logs"
RESULTS_DIR = REPO_ROOT / "results"
