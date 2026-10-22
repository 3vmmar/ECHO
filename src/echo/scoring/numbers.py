"""Deterministic number normalizer for echo.scoring (internal to the package).

Converts digit glyphs and recognized Egyptian Arabic cardinal-number
expressions to digits. Unsupported or ambiguous forms are left unchanged and
their errors are reported. The grammar and its tests are frozen on
development data.
"""
