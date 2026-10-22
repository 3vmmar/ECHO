"""Local diary storage under ECHO_DATA/diary.

Planned interface
- save(audio, transcript, system): the new entry id. Keeps the original ASR
  text alongside the edited transcript.
- update(entry_id, transcript): store an edited transcript.
- entries(): saved entries, newest first.
- delete(entry_id): remove the audio file and its record permanently.
"""
