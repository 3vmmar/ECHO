"""LoRA adaptation of Whisper Small on the diary training speakers only.

Planned interface
- train(config, train_clips, val_clips): one training run. Returns the best
  checkpoint by validation strict WER, the training curve and peak GPU memory.

The config (rank, target modules, learning rate, maximum steps, seed) is a
JSON file in configs/lora/. Early stopping and model selection use validation
speakers only. Every run is logged through echo.records, including failed ones.
"""
