"""Build and certify this longitudinal overgen pole."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from wager.factory.overgen_stream_tools import build_and_check

if __name__ == "__main__":
    build_and_check(Path(__file__).parent)
