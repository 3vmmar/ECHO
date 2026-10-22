"""The single scoring function, applied identically to references and to every system.

Planned interface
- SCORER_VERSION: changed on any rule change and frozen before test inference.
- normalize(text, relaxed=False): the text the scorer compares.
- score(references, hypotheses, relaxed=False): word and character error
  counts (substitutions, deletions, insertions, reference length), from which
  WER and CER follow. CER is computed without spaces.

Callers and tests import only from echo.scoring. The modules normalize,
numbers and align are internal to this package.

Strict rules (the primary score)
- Remove diacritics and Tatweel.
- Fold Alef variants to bare Alef and final Alef Maqsura to Ya. Keep Ta
  Marbuta distinct from Ha.
- Remove punctuation and standardize whitespace.
- Canonicalize digit glyphs and recognized cardinal-number expressions to digits.
- Keep English words in Latin script, lowercased.
- Drop the non-lexical hesitations listed in configs/scoring/hesitations.txt.
- No automatic clitic splitting; the transcription guide decides clitic spacing.

Relaxed rules (a sensitivity check only)
- The strict rules plus word-final Ta Marbuta/Ha folding and the alternative
  spellings in configs/scoring/alt_spellings.tsv.
"""
