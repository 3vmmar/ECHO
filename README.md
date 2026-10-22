# ECHO (DSAI 456)
Emotion-aware Egyptian Arabic voice diary.

Systems: A = openai/whisper-small, B = MAdel121/whisper-small-egyptian-arabic, C = A + LoRA on diary training data.

Layout
- configs/   frozen protocol, speaker split, manifest header
- src/echo/  shared code
- scripts/   numbered runnable scripts
- logs/      experiment records and environment info
- results/   metrics and tables

Data lives OUTSIDE this repo at C:\ECHO_DATA (override with env var ECHO_DATA).
Never commit audio, consent forms, or checkpoints.
