"""The diary and emotion corpora, read from the manifests in ECHO_DATA/manifests.

Planned interface
- diary_clips(partition): clips with speaker_id, clip_id, wav_path, reference
  text, mixed_language and status. The reference is the adjudicated transcript
  when one exists, otherwise the first pass.
- emotion_clips(partition): clips with speaker_id, clip_id, sentence_id,
  intended_style and take.
- check(): a list of problems, empty when the corpus is consistent. Covers
  speakers outside configs/split.json or in two partitions, clips outside
  5 to 20 seconds, missing or non-16 kHz mono audio, duplicate clip ids and
  missing transcripts. Reads every partition for structure only.

Invariant: requesting the "test" partition raises unless configs/frozen.json
exists. This module is the single place that enforces "test speakers are used
only for the final evaluation".
"""
