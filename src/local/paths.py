"""
Paths used throughout
"""

from __future__ import annotations

from pathlib import Path

HERE = Path(__file__)
ROOT = HERE.parents[2]

DATA_DIR = ROOT / "data"

ESGF_INTAKE_PATH = DATA_DIR / "esgf-intake"
ESGF_INTAKE_DB_PATH = ESGF_INTAKE_PATH / "db.db"
ESGF_INTAKE_DOWNLOAD_PATH = ESGF_INTAKE_PATH / "downloaded"

TIMESERIES_DB_PATH = DATA_DIR / "interim" / "timeseries_db"
