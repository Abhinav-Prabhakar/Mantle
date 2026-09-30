"""Mantle ML: models M0-M6, optimisers O1-O3, registry and CLI.

OpenMP note (macOS): PyTorch and LightGBM/scikit-learn each bundle their own libomp; mixing them in one process crashes
or deadlocks unless (a) ``lightgbm`` is imported before ``torch`` and (b) torch runs single-threaded. The trainer
therefore runs every model in its own subprocess (M3 alone gets 8 torch threads) and the registry imports lightgbm first.
"""

__version__ = "0.1.0"
