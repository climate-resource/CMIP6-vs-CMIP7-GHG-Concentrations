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
# # Grab Western et al., 2024 data
#
# Original paper: https://doi.org/10.1038/s41558-024-02038-7
# Zenodo record: https://zenodo.org/records/10782689

# %%
import pandas as pd
import pooch

from utils import PROCESSED_DATA_DIR

# %%
raw_data_file = pooch.retrieve(
    "https://zenodo.org/records/10782689/files/Projections.zip?download=1",
    known_hash="10ffeebdcfd362186ce64abb1dc1710e3ebf4d6b41bf18faf2bb7ff45a82b2f7",
    processor=pooch.Unzip(members=["Projections/hcfc_projections_v2.csv"]),
)
if len(raw_data_file) != 1:
    raise AssertionError

raw_data_file = raw_data_file[0]
raw_data_file

# %%
raw = pd.read_csv(raw_data_file, skiprows=1)
raw

# %%
out_file = PROCESSED_DATA_DIR / "western-et-al-2024" / "hcfc_projections.csv"
out_file.parent.mkdir(exist_ok=True, parents=True)
raw.to_csv(out_file, index=False)
