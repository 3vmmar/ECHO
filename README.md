# ECHO

**An emotion-aware Egyptian Arabic voice diary built on dialect-adaptive speech recognition.**

ECHO is a DSAI 456 course project. A student records a short spoken diary entry (about 5 to 20 seconds), the app transcribes it, and the student can edit the transcript, replay the audio, save the entry and delete it. Everything runs locally.

The main task is accurate Egyptian Arabic transcription. A secondary classifier shows the expressed vocal style (happy, sad, angry or neutral), and optional text sentiment is shown separately. Neither output is a diagnosis or a measure of how the user actually feels.

> **Status: early development.** This repository holds the project protocol, the frozen speaker split, environment records and GPU profiling. It contains no audio, transcripts, checkpoints or results.

## Research question

Does diary-specific LoRA adaptation improve transcription of Egyptian Arabic speakers the model has never heard, and how does it compare with an existing Egyptian Arabic recognizer? The study is a controlled domain-adaptation comparison, not a new architecture.

| System | Model | Training |
|---|---|---|
| A | [`openai/whisper-small`](https://huggingface.co/openai/whisper-small) | None |
| B | [`MAdel121/whisper-small-egyptian-arabic`](https://huggingface.co/MAdel121/whisper-small-egyptian-arabic) | None, evaluated as published |
| C | `openai/whisper-small` + LoRA | Own diary training data only |

All three systems receive identical audio and identical decoding settings:

| Setting | Value |
|---|---|
| Language / task | Arabic / transcribe |
| Decoding | Beam size 5, no sampling (temperature 0 where supported) |
| Timestamps | Off |
| Prompt | None |
| Previous-text conditioning | Off |
| Audio | 16 kHz, mono |

The settings are defined in [`configs/protocol.json`](configs/protocol.json), currently marked `v0-draft`.

## Evaluation protocol

- One versioned scoring function is applied identically to the references and to all three systems. It is frozen on development data before any test run.
- The primary score is pooled strict WER. CER is reported as well. A relaxed WER (word-final Ta Marbuta/Ha folding and a reviewed list of alternative spellings) is a sensitivity check only.
- The test speakers are used only for the final evaluation. Test audio, references and predictions are never used to choose a model, change normalization rules or change decoding.
- LoRA settings (rank, adapted layers, learning rate, training length) are chosen using training and validation data only, then frozen before the test run. Every run is logged, including failures.
- Uncertainty is reported as paired WER differences with 95% percentile intervals from 2,000 bootstrap resamples of whole test speakers.

**Success target.** At least a 10% relative reduction in pooled strict WER for C versus A, improvement on at least 5 of the 6 test speakers, and a positive reduction under relaxed scoring. This is a target, not a prediction, and all outcomes will be reported.

## Data

The corpus is collected for this project and is not included in the repository.

- 24 consenting adult Egyptian Arabic speakers, about 10 usable minutes each, speaking naturally rather than reading. Recordings are cut into 5 to 20 second clips and exported as 16 kHz mono WAV.
- Speakers are split 14 train, 4 validation and 6 test. A speaker never appears in more than one partition. The assignment is fixed in [`configs/split.json`](configs/split.json) (seed 42), and the script that creates it refuses to run again.
- For the emotion model, the same speakers record 8 neutral sentences in 4 acted styles, twice (1,536 clips), using the same split. Labels describe intended acted expression.
- Public Arabic datasets are not used in the main experiment.

Data is private, consented and for academic use only. It lives outside the repository at `C:\ECHO_DATA`, which can be relocated with the `ECHO_DATA` environment variable.

```
C:\ECHO_DATA
├── consent/     consent records
├── raw/         original recordings
├── wav16k/      converted 16 kHz mono audio
├── clips/       5 to 20 second clips
├── emotion/     acted-emotion recordings
└── manifests/   clip manifests
```

Audio, consent records, checkpoints and predictions are never committed, and `.gitignore` blocks the common file types.

## Repository layout

```
ECHO/
├── configs/
│   ├── protocol.json          Fixed decoding settings and system definitions
│   ├── split.json             Frozen speaker-to-partition assignment
│   └── manifest_header.csv    Column header for the clip manifest
├── logs/                      Environment records and experiment logs
├── results/                   Metrics and tables (empty for now)
├── scripts/                   Numbered, runnable scripts
├── src/echo/                  Shared code (data paths so far)
├── tests/                     Unit tests (empty for now)
├── requirements.txt           Pinned package versions
├── LICENSE
└── README.md
```

## Getting started

Developed on Windows 11 with Python 3.13 and an NVIDIA RTX 3070 Laptop GPU (8 GB, CUDA 12.4). From the repository root in PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
```

| Script | Purpose |
|---|---|
| `scripts/00_env_info.py` | Records Python, CUDA, GPU and package versions to `logs/env_info.json` |
| `scripts/01_make_split.py` | Creates `configs/split.json` with seed 42. Stops if the file already exists |
| `scripts/02_gpu_profile.py` | Measures peak GPU memory and step time for Whisper Small with LoRA. Writes `logs/gpu_profile.json` |

## Compute

At batch size 1 with gradient checkpointing and bf16 autocast, Whisper Small with LoRA peaked at roughly 2.1 to 2.7 GB of GPU memory across ranks 8 to 32 and both adapter scopes tried (attention-only and all linear layers). It fits the 8 GB card with room to spare, so no smaller-model fallback is planned. These figures use synthetic inputs at the full padded length and measure memory and speed only. Details are in `logs/gpu_profile.json`.

## Roadmap

- [x] Environment and package versions recorded
- [x] Speaker split fixed (14 / 4 / 6)
- [x] GPU memory profiling
- [ ] Scoring and data tools: normalization, WER and CER, manifest checks, audio conversion, inference runner for A, B and C
- [ ] Pilot: confirm B runs, time transcription, draft scoring rules on pilot data only
- [ ] LoRA training with validation-based selection and early stopping
- [ ] Final evaluation with a paired bootstrap over whole test speakers
- [ ] Vocal-style classifier (SVM on MFCC and prosody features)
- [ ] Local diary app with editing, playback, save and delete

## Limitations

- Six test speakers give unstable intervals and no population-level conclusions. A 5-of-6 improvement pattern is a consistency target, not a significance claim.
- Adaptation can teach a model the project's spelling conventions as well as improve acoustic recognition. The relaxed-WER check exists to expose gains that depend on convention.
- The vocal-style classifier is trained on acted expression and is not validated on natural diary speech.
- The optional text sentiment output is an unevaluated demonstration feature.

## Team

| Member | Responsibility |
|---|---|
| Ammar Ahmed | ASR baselines, LoRA adaptation and integration |
| Youssef Mahmoud | Recruitment, consent, first-pass transcription and preprocessing |
| Mariam Zakary | Independent annotation review and vocal-emotion modelling |
| Mostafa Magdy | Annotation adjudication, evaluation and application demo |

## References

1. Radford et al. (2023). [Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356). ICML.
2. Hu et al. (2022). [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685). ICLR.
3. Habash, Diab and Rambow (2012). [Conventional Orthography for Dialectal Arabic](https://aclanthology.org/L12-1328/). LREC.

## License

The code is released under the [MIT License](LICENSE). The license does not cover the corpus, which is private and not distributed.
