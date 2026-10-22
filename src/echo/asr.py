"""Speech recognition systems A, B and C under the fixed decoding protocol.

Planned interface
- Recognizer(system, adapter_dir=None): "A" is openai/whisper-small, "B" is
  MAdel121/whisper-small-egyptian-arabic and "C" is Whisper Small plus the
  LoRA adapter in adapter_dir.
- Recognizer.transcribe(audio): the transcript as a string.

Decoding settings come only from configs/protocol.json (Arabic, transcribe,
beam size 5, no sampling, no timestamps, no prompt, no previous-text
conditioning) and are identical for every system. Model revisions and
generation settings are recorded with every prediction file.
"""
