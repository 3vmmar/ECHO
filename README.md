# ECHO

**An emotion-aware Egyptian Arabic voice diary built on dialect-adaptive speech recognition.**

ECHO is a DSAI 456 course project. A student records a short spoken diary entry (about 5 to 20 seconds), the app transcribes it, and the student can edit the transcript, replay the audio, save the entry and delete it. Everything runs locally.

The main task is accurate Egyptian Arabic transcription. A secondary classifier shows the expressed vocal style (happy, sad, angry or neutral), and optional text sentiment is shown separately. Neither output is a diagnosis or a measure of how the user actually feels.

> **Status: early development.** This repository holds the project protocol, the frozen speaker split, environment records, GPU profiling and the planned code structure. Modules and notebooks describe what they will do but are not implemented yet. The repository contains no audio, transcripts, checkpoints or results.

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
├── manifests/   clip manifests and transcripts
├── predictions/ model outputs, written once
├── checkpoints/ LoRA adapters
└── diary/       entries saved by the app
```

Audio, consent records, checkpoints and predictions are never committed, and `.gitignore` blocks the common file types. File naming, manifest columns and consent handling are described in [`docs/data_protocol.md`](docs/data_protocol.md), and the spelling conventions in [`docs/transcription_guide.md`](docs/transcription_guide.md).

## Repository layout

```
ECHO/
├── app/                       Local diary app (Phase 6)
├── configs/
│   ├── protocol.json          Fixed decoding settings and system definitions
│   ├── split.json             Frozen speaker-to-partition assignment
│   ├── *_header.csv           Column headers for the manifests and transcripts
│   ├── emotion_sentences.csv  The 8 fixed emotion-corpus sentences
│   ├── scoring/               Hesitation list and alternative spellings
│   └── lora/                  One JSON file per LoRA training configuration
├── docs/                      Data protocol, transcription guide, decision log
├── logs/                      Environment records, GPU profile, run logs
├── notebooks/                 One notebook per phase
├── results/                   Tables and figures (no transcripts)
├── scripts/                   Numbered, runnable scripts
├── src/echo/
│   ├── paths.py               Data and repository locations
│   ├── records.py             Write-once outputs, run log, seeds
│   ├── audio.py               Audio conversion and loading
│   ├── corpus.py              Clips and references by partition, test-partition guard
│   ├── scoring/               The single scoring function
│   ├── asr.py                 Systems A, B and C under the fixed protocol
│   ├── lora.py                LoRA training with validation early stopping
│   ├── evaluation.py          Result tables, paired speaker bootstrap, success criteria
│   ├── emotion.py             Vocal-style features and SVM
│   ├── sentiment.py           Optional text sentiment
│   └── diary.py               Local diary storage
├── tests/                     Unit tests through each module's interface
├── pyproject.toml             Package and pytest settings
├── requirements.txt           Pinned package versions
├── LICENSE
└── README.md
```

Each module's docstring states its planned interface. Callers and tests use only that interface; for example, the number normalizer and alignment code inside `scoring/` are reached through `normalize()` and `score()`. `corpus.py` is the single place that refuses the test partition until the protocol is frozen.

## Getting started

Developed on Windows 11 with Python 3.13 and an NVIDIA RTX 3070 Laptop GPU (8 GB, CUDA 12.4). From the repository root in PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
pip install -e .
```

`pip install -e .` makes `src/echo` importable from scripts, notebooks and tests. Run the tests with `python -m pytest`.

| Script | Purpose | Status |
|---|---|---|
| `scripts/00_env_info.py` | Records Python, CUDA, GPU and package versions to `logs/env_info.json` | Ready |
| `scripts/01_make_split.py` | Creates `configs/split.json` with seed 42. Stops if the file already exists | Ready, already run |
| `scripts/02_gpu_profile.py` | Measures peak GPU memory and step time for Whisper Small with LoRA. Writes `logs/gpu_profile.json` | Ready, already run |
| `scripts/03_convert_audio.py` | Converts raw recordings to 16 kHz mono WAV | Planned, phase 1 |
| `scripts/04_check_corpus.py` | Checks the manifests against the speaker split | Planned, phase 1 |
| `scripts/05_transcribe.py` | Transcribes a partition with A, B or C | Planned, phase 1 |
| `scripts/06_score.py` | Scores predictions: strict WER, relaxed WER and CER | Planned, phase 1 |
| `scripts/07_train_lora.py` | Trains one LoRA configuration with validation early stopping | Planned, phase 3 |
| `scripts/08_freeze_protocol.py` | Freezes the scorer, protocol and selected checkpoint before testing | Planned, phase 3 |
| `scripts/09_final_evaluation.py` | Final held-out evaluation with the paired bootstrap | Planned, phase 4 |
| `scripts/10_train_emotion.py` | Trains and evaluates the vocal-style classifier | Planned, phase 5 |

## Notebooks

One notebook per phase in `notebooks/`, from `00_corpus_overview` to `06_usability_study`. Each holds a section outline for now and will call the code in `src/echo`. Notebook outputs can contain private transcripts, so clear all outputs before committing.

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
