"""Train one LoRA configuration from configs/lora/ on the training speakers.

Phase 3, not implemented yet. Selects the checkpoint by validation strict WER
with early stopping, saves it to ECHO_DATA/checkpoints and logs the run,
including failures, to logs/runs/.
"""
