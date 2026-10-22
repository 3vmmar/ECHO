import json
import sys
import time
from pathlib import Path

import peft
import torch
import transformers
from peft import LoraConfig, get_peft_model
from transformers import WhisperForConditionalGeneration

SEED = 42
STEPS = 6  # the first step is warm-up and is excluded from the mean
BATCH, MEL_FRAMES, LABEL_TOKENS = 1, 3000, 80
LR = 1e-4
RANKS = (8, 16, 32)
ATTN = ["q_proj", "v_proj"]
ALL = ["q_proj", "k_proj", "v_proj", "out_proj", "fc1", "fc2"]

OUT = Path(__file__).resolve().parents[1] / "logs" / "gpu_profile.json"

if OUT.exists():
    print(f"STOP: {OUT} already exists. Move or rename it to keep both records.")
    sys.exit(1)
if not torch.cuda.is_available():
    print("STOP: CUDA is not available.")
    sys.exit(1)


def profile(rank, targets):
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    torch.manual_seed(SEED)
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small").to("cuda")
    model.config.use_cache = False
    model.gradient_checkpointing_enable()
    model.enable_input_require_grads()
    model = get_peft_model(model, LoraConfig(r=rank, lora_alpha=2 * rank,
                           target_modules=targets, lora_dropout=0.05, bias="none"))
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=LR)
    features = torch.randn(BATCH, 80, MEL_FRAMES, device="cuda")
    labels = torch.randint(0, 50000, (BATCH, LABEL_TOKENS), device="cuda")
    times = []
    for _ in range(STEPS):
        torch.cuda.synchronize()
        t = time.time()
        with torch.autocast("cuda", dtype=torch.bfloat16):
            loss = model(input_features=features, labels=labels).loss
        loss.backward()
        opt.step()
        opt.zero_grad()
        torch.cuda.synchronize()
        times.append(time.time() - t)
    result = {
        "rank": rank,
        "target_modules": targets,
        "peak_gb": round(torch.cuda.max_memory_allocated() / 1e9, 2),
        "step_s": round(sum(times[1:]) / len(times[1:]), 3),
    }
    del model, opt
    torch.cuda.empty_cache()
    return result


runs = []
for rank in RANKS:
    for targets in (ATTN, ALL):
        run = profile(rank, targets)
        print(f"r={run['rank']:>2} modules={len(targets)} peak={run['peak_gb']:.2f} GB  step={run['step_s']:.2f}s")
        runs.append(run)

info = {
    "note": ("Synthetic inputs (random mel features and token ids) padded to the full 30 s "
             "encoder length. Measures memory and speed only, not training quality."),
    "seed": SEED,
    "model": "openai/whisper-small",
    "gpu": torch.cuda.get_device_name(0),
    "vram_gb": round(torch.cuda.get_device_properties(0).total_memory / 1e9, 2),
    "versions": {
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "peft": peft.__version__,
    },
    "settings": {
        "batch_size": BATCH,
        "mel_frames": MEL_FRAMES,
        "label_tokens": LABEL_TOKENS,
        "weights": "fp32",
        "autocast": "bf16",
        "gradient_checkpointing": True,
        "optimizer": "AdamW",
        "lr": LR,
        "lora_alpha": "2 x rank",
        "lora_dropout": 0.05,
        "steps": STEPS,
        "warmup_steps_excluded": 1,
    },
    "runs": runs,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(info, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
