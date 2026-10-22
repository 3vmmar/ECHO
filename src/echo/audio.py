"""Audio conversion and loading.

Planned interface
- convert(src, dst): any input format to 16 kHz mono WAV through ffmpeg. Never
  modifies src and never overwrites dst.
- load(path): the clip as a NumPy array at 16 kHz mono. Raises if the file is
  not 16 kHz mono, so every system receives identical input.
"""
