"""Train and evaluate the vocal-style classifier.

Phase 5, not implemented yet. Fits feature scaling and the SVM on training
speakers, chooses settings on validation speakers, then scores the test
speakers once: macro-F1, per-class precision and recall, and a confusion
matrix against a class-frequency dummy baseline.
"""
