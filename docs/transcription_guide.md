# Transcription guide

A CODA-informed spelling guide for Egyptian Arabic diary clips (Habash, Diab and Rambow, 2012). Sections marked **Team decision** are still to be agreed. Record each agreement in `docs/decisions.md`.

## Ground rules

These come from the project proposal and are fixed.

- Transcribe from the audio only. Never start from ASR output.
- Write readable canonical spelling. Do not strip diacritics or fold letters by hand, because the scorer normalizes references and model outputs the same way.
- Log unintelligible or overlapping clips (`status = excluded` with a reason) and decide on them without looking at any model output.

## Clitics

**Team decision:** which clitics attach to their host word and which stand alone. The scorer does not split clitics, so this guide alone decides word boundaries.

## English words

Write English words in Latin script as spoken. The scorer lowercases them.

## Repetitions, fillers and hesitations

- Keep audible complete-word repetitions and lexical fillers.
- **Team decision:** one fixed spelling for each non-lexical hesitation sound, so the scorer can drop them using `configs/scoring/hesitations.txt`.

## Numbers

**Team decision:** digits or words. The scorer converts digit glyphs and recognized number expressions to digits on both sides, but a consistent choice keeps references readable.

## Non-speech events

**Team decision:** how to mark laughter, coughs and background noise. These events are logged separately and are not scored as words.

## Second annotation and adjudication

- At least 25% of clips, sampled across speakers and partitions, are transcribed a second time independently, without seeing the first pass.
- Disagreements are adjudicated by listening.
- Word disagreement before adjudication is reported.
