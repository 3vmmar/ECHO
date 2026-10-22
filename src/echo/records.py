"""Experiment records: write-once outputs, the run log and environment snapshots.

Planned interface
- write_once(path, data): write JSON or text and raise if the file already
  exists. Used for predictions, frozen configs and final results, so nothing
  saved is ever overwritten.
- log_run(record): append one JSON line to logs/runs/ for every training or
  inference run, including failed ones.
- snapshot(): Python, CUDA, GPU and package versions plus the git commit.
- set_seed(seed): seed Python, NumPy and PyTorch.
"""
