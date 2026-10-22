"""Freeze the evaluation protocol before any test inference.

Phase 3, not implemented yet. Writes configs/frozen.json with the scorer
version, hashes of the protocol and scoring lists, and the selected LoRA run
and checkpoint hash. Refuses to run if the file already exists.
"""
