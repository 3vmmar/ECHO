# Data protocol

How ECHO data is named, stored and tracked. The DSAI 456 project proposal is the source of truth; this page records how the team applies it.

## Storage

All data lives in `C:\ECHO_DATA` (or the folder named by the `ECHO_DATA` environment variable), never in the repository.

| Folder | Contents |
|---|---|
| `consent/` | Consent records and the private key linking people to speaker IDs |
| `raw/` | Original recordings, never modified |
| `wav16k/` | 16 kHz mono conversions of the originals |
| `clips/` | Diary clips of 5 to 20 seconds |
| `emotion/` | Acted-emotion clips |
| `manifests/` | `diary_manifest.csv`, `transcripts.csv`, `emotion_manifest.csv` |
| `predictions/` | Model outputs, written once and never overwritten |
| `checkpoints/` | LoRA adapters |
| `diary/` | Entries saved by the local app |

## Speaker IDs

- Speakers get pseudonymous IDs `S01` to `S24` in recruitment order. The partition for each ID is fixed in `configs/split.json` (14 train, 4 validation, 6 test).
- The key linking people to IDs stays in `consent/`.
- Pilot speakers are never given a test-partition ID.

## File names (proposed)

- Diary clips: `<speaker>_<4-digit index>.wav`, for example `S07_0012.wav`.
- Emotion clips: `<speaker>_E<sentence>_<style>_<take>.wav`, for example `S07_E3_sad_2.wav`.

## Manifests

Column headers live in `configs/`. Fill one row per clip.

**Diary manifest** (`configs/manifest_header.csv`)

| Column | Meaning |
|---|---|
| `speaker_id` | `S01` to `S24` |
| `partition` | `train`, `val` or `test`; must match `configs/split.json` |
| `clip_id` | Unique clip name, for example `S07_0012` |
| `source_recording` | Raw file that `start` and `end` refer to |
| `start`, `end` | Clip boundaries in seconds within the source recording |
| `duration` | Clip length in seconds (5 to 20) |
| `environment` | Recording conditions |
| `wav_path` | Clip path relative to `ECHO_DATA` |
| `transcript_version` | Transcript version used as the reference |
| `mixed_language` | `1` if the clip contains English words, else `0` |
| `second_annotated` | `1` if the clip is in the independent second-annotation sample, else `0` |
| `status` | `ok` or `excluded` |
| `exclusion_reason` | For excluded clips: `unintelligible`, `overlap` or another short reason |

**Transcripts** (`configs/transcripts_header.csv`)

| Column | Meaning |
|---|---|
| `clip_id` | Matches the diary manifest |
| `transcript_version` | Version label |
| `pass` | `first`, `second` or `adjudicated` |
| `annotator` | Annotator initials |
| `text` | The transcript, written according to `docs/transcription_guide.md` |

**Emotion manifest** (`configs/emotion_manifest_header.csv`)

| Column | Meaning |
|---|---|
| `speaker_id`, `partition` | As in the diary manifest |
| `clip_id` | Unique clip name |
| `sentence_id` | 1 to 8, matching `configs/emotion_sentences.csv` |
| `intended_style` | `happy`, `sad`, `angry` or `neutral` |
| `take` | `1` or `2` |
| `duration`, `wav_path`, `status`, `exclusion_reason` | As in the diary manifest |

## Consent and withdrawal

- Consent covers collection, transcription, model training, retention through course assessment and deletion within 90 days after final grading. Demo playback is consented to separately.
- A withdrawal, including after data is frozen, removes that person's data and triggers a documented revision or rerun, recorded in `docs/decisions.md`.

## Notebook outputs

Notebook outputs can contain private transcripts. Clear all outputs before committing a notebook.
