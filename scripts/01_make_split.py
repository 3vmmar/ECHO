import json
import random
import sys
from pathlib import Path

SEED = 42
N_TRAIN, N_VAL, N_TEST = 14, 4, 6
OUT = Path(__file__).resolve().parents[1] / "configs" / "split.json"

if OUT.exists():
    print(f"STOP: {OUT} already exists. The split is frozen and must not be regenerated.")
    sys.exit(1)

ids = [f"S{i:02d}" for i in range(1, N_TRAIN + N_VAL + N_TEST + 1)]
random.Random(SEED).shuffle(ids)

split = {
    "seed": SEED,
    "train": sorted(ids[:N_TRAIN]),
    "val": sorted(ids[N_TRAIN:N_TRAIN + N_VAL]),
    "test": sorted(ids[N_TRAIN + N_VAL:]),
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(split, indent=2), encoding="utf-8")
print(json.dumps(split, indent=2))
