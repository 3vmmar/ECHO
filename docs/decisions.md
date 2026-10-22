# Decision log

Every protocol decision, with the data it was based on. Test data is never a basis for a decision. Newest entries go at the bottom.

| Date | Decision | Based on | By |
|---|---|---|---|
| 2026-10-22 | Speaker split fixed with seed 42: 14 train, 4 validation, 6 test (`configs/split.json`) | Speaker IDs only, before any data | Ammar |
| 2026-10-22 | Keep Whisper Small for A and C; no Whisper Base fallback | GPU profile, peak 2.14 to 2.68 GB (`logs/gpu_profile.json`) | Ammar |
| 2026-10-22 | The scorer does no automatic clitic splitting; the transcription guide decides clitic spacing | Proposal section 4.2 | Ammar |
| 2026-10-22 | Diary manifest adds `source_recording`, `wav_path`, `mixed_language`, `second_annotated`, `status` and `exclusion_reason`; transcripts are kept in a separate file keyed by `clip_id` and `transcript_version` | Reporting needs in proposal sections 4.1 to 4.3 | Ammar |
