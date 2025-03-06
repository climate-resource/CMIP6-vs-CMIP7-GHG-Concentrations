"""
Our timeseries database
"""

from __future__ import annotations

from pathlib import Path

from pandas_openscm.db import (
    FeatherDataBackend,
    FeatherIndexBackend,
    OpenSCMDB,
    OpenSCMDBDataBackend,
    OpenSCMDBIndexBackend,
)

from local.paths import TIMESERIES_DB_PATH


def get_timeseries_db(
    db_dir: Path = TIMESERIES_DB_PATH,
    backend_data: OpenSCMDBDataBackend = FeatherDataBackend(),
    backend_index: OpenSCMDBIndexBackend = FeatherIndexBackend(),
) -> OpenSCMDB:
    """
    Get our timeseries database, with sensible defaults

    Parameters
    ----------
    db_dir
        Database directory

    backend_data
        Backend to use for saving data

    backend_index
        Backend to use for saving the index

    Returns
    -------
    :
        Database instance
    """
    return OpenSCMDB(
        db_dir=db_dir,
        backend_data=backend_data,
        backend_index=backend_index,
    )
