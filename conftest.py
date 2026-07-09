"""Ensures the repository root is importable as a package root for pytest (e.g. 'from src.data_quality.checks import ...')."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
