"""
Official Single Execution Entrypoint for SupeRR Selector Season 2 (V4 Multiverse Model).

Usage:
    python src/run_v4.py
"""
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.model_v4.run_multiverse_pipeline import main

if __name__ == "__main__":
    main()
