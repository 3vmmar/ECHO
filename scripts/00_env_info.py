import json
import platform
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import torch

PACKAGES = ["torch", "transformers", "peft", "accelerate", "huggingface_hub",
            "librosa", "numpy", "soundfile", "datasets"]


def pkg_version(name):
    try:
        return version(name)
    except PackageNotFoundError:
        return None


cuda = torch.cuda.is_available()
info = {
    "python": sys.version,
    "platform": platform.platform(),
    "cuda_available": cuda,
    "cuda_version": torch.version.cuda,
    "gpu": torch.cuda.get_device_name(0) if cuda else None,
    "vram_gb": round(torch.cuda.get_device_properties(0).total_memory / 1e9, 2) if cuda else None,
    "packages": {p: pkg_version(p) for p in PACKAGES},
}

out = Path(__file__).resolve().parents[1] / "logs" / "env_info.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(info, indent=2), encoding="utf-8")
print(json.dumps(info, indent=2))
