"""Module containing the paths"""
import os
from pathlib import Path

IPOPT_PATH = Path.home().parent.parent / "msys64" / "mingw64" / "bin" / "ipopt.exe"

PROJECT_PATH = Path(__file__).parent.parent
DATA_PATH = PROJECT_PATH / "data"