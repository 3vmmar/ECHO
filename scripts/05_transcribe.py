"""Transcribe one partition with system A, B or C.

Phase 1, not implemented yet. Writes predictions to ECHO_DATA/predictions with
the model revision, protocol hash and software versions. Refuses to overwrite
an existing prediction file, and refuses the test partition until
configs/frozen.json exists.

Planned usage: python scripts/05_transcribe.py --system A --partition val
"""
