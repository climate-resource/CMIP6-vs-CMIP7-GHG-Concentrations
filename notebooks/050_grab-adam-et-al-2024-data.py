# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Grab Adam et al., 2024 data
#
# Original paper: https://doi.org/10.1038/s43247-024-01946-y
# Raw data: passed to me via email (stored in repo)

# %%
import pandas as pd
import pooch

from utils import RAW_DATA_DIR, PROCESSED_DATA_DIR

# %%
raw_data_file = RAW_DATA_DIR / "adam-et-al-2024" / "HFC-23_Global_annual_mole_fraction.csv"
raw_data_file

# %%
with open(raw_data_file) as fh:
    raw_contents = fh.read()

if "Units: ppt" not in raw_contents:
    raise AssertionError
    
unit = "ppt"

# %%
raw = pd.read_csv(raw_data_file, comment="#")
out = raw.rename({"Year": "year", "Global_annual_mole_fraction": "hfc23"}, axis="columns")[["year", "hfc23"]]
out

# %%
out_file = PROCESSED_DATA_DIR / "adam-et-al-2024" / "hfc23_projections.csv"
out_file.parent.mkdir(exist_ok=True, parents=True)
out.to_csv(out_file, index=False)
