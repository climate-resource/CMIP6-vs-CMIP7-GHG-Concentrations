"""
Helper for intake-esgf

Sets a few sensible defaults so we don't have to repeat them everywhere
"""

from __future__ import annotations

from pathlib import Path

import intake_esgf

from local.paths import ESGF_INTAKE_DB_PATH, ESGF_INTAKE_DOWNLOAD_PATH


def set_intake_esgf_conf_defaults(
    local_cache: Path | None = ESGF_INTAKE_DOWNLOAD_PATH,
    download_db: Path | None = ESGF_INTAKE_DB_PATH,
    set_default_indexes: bool = True,
) -> None:
    """
    Set intake ESGF's config to sensible defaults

    Parameters
    ----------
    local_cache
        Location into which to download data

        If not supplied, we use intake-esgf's defaults.

    download_db
        Database to use to store information about downloads etc.

        If not supplied, we use intake-esgf's defaults.

    set_default_indexes
        Should we set default indexes from which to retrieve data.
    """
    if local_cache is not None:
        intake_esgf.conf.set(local_cache=local_cache)
    # I don't think they want you to do this,
    # but for our use case (complete isolation) it makes sense
    # and people can always do something else if they want.
    if download_db is not None:
        intake_esgf.conf["download_db"] = download_db

    if set_default_indexes:
        intake_esgf.conf.set(
            indices={"esgf-node.llnl.gov": True, "esgf1.dkrz.de": True}
        )
