"""
Time handling helpers
"""

from __future__ import annotations

import pandas as pd


def convert_time_cols_to_plotting_float(
    indf: pd.DataFrame, *, frequency: str
) -> pd.DataFrame:
    """
    Convert columns of a [pd.DataFrame][pandas.DataFrame] to useful floats for plotting

    Parameters
    ----------
    indf
        Input [pd.DataFrame][pandas.DataFrame]

    frequency
        Frequency of the data

    Returns
    -------
    :
        [pd.DataFrame][pandas.DataFrame] with converted columns
    """
    out = indf

    if frequency == "yr":
        out.columns = out.columns.map(lambda x: x.year + 1 / 2)

    elif frequency == "mon":
        out.columns = out.columns.map(lambda x: x.year + x.month / 12 + 1 / 24)

    else:
        raise NotImplementedError

    return out
