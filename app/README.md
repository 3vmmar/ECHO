# Diary app

Phase 6. A local app for recording and correcting diary entries. It is not built yet, and the UI stack is chosen at the start of Phase 6. Storage lives in `src/echo/diary.py`.

## Required features

- Record a 5 to 20 second entry and transcribe it.
- Edit the transcript, keeping the original ASR text alongside the edit.
- Replay, save and delete entries. Delete removes the audio and the text permanently.
- Show the expressed vocal style, labelled as a description of the voice, not of the user's feelings.
- Optionally show text sentiment separately, labelled as an unevaluated demonstration. The two outputs are never merged into a mood score.

## Usability study mode

Each participant corrects matched clips transcribed by A and by C, with assignment and order counterbalanced and the model hidden. The app logs correction seconds per audio minute and whether edit, save, replay and delete were completed.
