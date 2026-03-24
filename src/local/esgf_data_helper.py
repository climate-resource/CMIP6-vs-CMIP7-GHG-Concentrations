"""
Helpers for working with ESGF data
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import pandas as pd
import xarray as xr
from input4mips_validation.cvs.drs import DataReferenceSyntax

DEFAULT_DRS = DataReferenceSyntax(
    directory_path_template="<activity_id>/<mip_era>/<target_mip>/<institution_id>/<source_id>/<realm>/<frequency>/<variable_id>/<grid_label>/v<version>",
    directory_path_example="not_used",
    filename_template="<variable_id>_<activity_id>_<dataset_category>_<target_mip>_<source_id>_<grid_label>[_<time_range>].nc",
    filename_example="not_used",
)
"""
Default DRS for working with local input4MIPs data
"""


def build_metadata_table(
    paths: Iterable[Path],
    drs: DataReferenceSyntax,
) -> pd.DataFrame:
    """
    Build a metadata table

    Parameters
    ----------
    paths
        Paths from which to get metadata

    drs
        DRS to use for extracting metadata

    Returns
    -------
    :
        Table of metadata
    """
    metadata_l = []
    for file in paths:
        metadata = (
            # A little bit dangerous as clashes aren't flagged
            drs.extract_metadata_from_path(file.parent)
            | drs.extract_metadata_from_filename(file.name)
            | xr.open_dataset(file, decode_times=False).attrs
        )
        metadata["filepath"] = str(file)
        metadata_l.append(metadata)

    return pd.DataFrame(metadata_l)
