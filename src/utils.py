"""Utility functions for reproducibility."""
from pathlib import Path
import random
import numpy as np
import yaml
import os

# Optional imports
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


def set_seed(seed: int = 42):
    """Set random seeds for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)

    if TORCH_AVAILABLE:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    print(f"Random seed set to {seed}")


def load_config(config_path: str = "config/config.yaml") -> dict:
    """Load configuration from a YAML file.

    Args:
        config_path: Path to config YAML file.

    Returns:
        Parsed config as a dictionary.

    Raises:
        FileNotFoundError: If config file does not exist.
        ValueError: If YAML cannot be parsed.
    """
    path = Path(config_path)

    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    try:
        with path.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise ValueError(f"Error parsing YAML config: {exc}") from exc

    if config is None:
        config = {}

    return config


__all__ = ["set_seed", "load_config"]
