"""Final comparison of A, B and C on the held-out test speakers.

Planned interface
- tables(scores): pooled and per-speaker WER and CER, strict and relaxed, with
  mixed-language utterances reported separately.
- bootstrap(scores, system_a, system_b, resamples=2000, seed): the paired
  pooled WER difference and its 95% percentile interval. Each resample draws
  whole test speakers with all their clips and pairs the systems within it.
- success(scores): the three proposal criteria for C versus A. At least a 10%
  relative reduction in pooled strict WER, improvement on at least 5 of the 6
  test speakers, and a positive reduction under relaxed scoring.
"""
