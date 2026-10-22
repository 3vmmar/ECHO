"""Vocal-style classifier for acted clips: happy, sad, angry or neutral.

Planned interface
- features(audio): an MFCC and prosody feature vector.
- train(train_clips, val_clips): a fitted scaler and SVM. The scaler is fit on
  training speakers only and SVM settings are chosen on validation speakers.
- predict(model, audio): a style label.

Reported with four-class macro-F1, per-class precision and recall and a
confusion matrix, against a class-frequency dummy baseline. The label
describes expressed vocal style, never the speaker's feelings.
"""
