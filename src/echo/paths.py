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
PREDICTIONS_DIR = DATA_ROOT / "predictions"
CHECKPOINTS_DIR = DATA_ROOT / "checkpoints"
DIARY_DIR = DATA_ROOT / "diary"

CONFIG_DIR = REPO_ROOT / "configs"
SCORING_CONFIG_DIR = CONFIG_DIR / "scoring"
LORA_CONFIG_DIR = CONFIG_DIR / "lora"
LOG_DIR = REPO_ROOT / "logs"
RUNS_DIR = LOG_DIR / "runs"
RESULTS_DIR = REPO_ROOT / "results"
TABLES_DIR = RESULTS_DIR / "tables"
FIGURES_DIR = RESULTS_DIR / "figures"
