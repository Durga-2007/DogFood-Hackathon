"""
Pytest configuration. Ensures src/ is on the Python path.
"""
import sys
import os
from pathlib import Path

# Add src to sys.path so test files can import from it
src_path = str(Path(__file__).parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)
