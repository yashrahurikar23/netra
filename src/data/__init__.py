"""
Data initialization and management for the Netra platform.
"""

from .loader import DataLoader
from .synthetic import SyntheticDataGenerator

__all__ = ["DataLoader", "SyntheticDataGenerator"]
