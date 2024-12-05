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
# # Grab Droste et al., 2020 data
#
# Original paper: https://doi.org/10.5194/acp-20-4787-2020
# Zenodo record: https://zenodo.org/records/3519317

# %%
from pathlib import Path

import pandas as pd
import pooch

from utils import PROCESSED_DATA_DIR

# %%
raw_data_files_l = pooch.retrieve(
    url="https://zenodo.org/records/3519317/files/Trends-Emission_PFCs_Droste-etal_ACP_20191025.zip?download=1",
    known_hash="f71fda6b8848f627b7736870241bfa075d941bcd458fff6105287e951aed6c21",
    processor=pooch.Unzip(
        members=["best-fits_CG_PFCs.csv", "best-fits_TAC_PFCs.csv"]
    ),
    progressbar=True,
)

raw_data_files_l

# %%
out_l = []
for file in raw_data_files_l:
    file = Path(file)
    if file.name.startswith("best-fits_CG"):
        # Cape grim lat
        lat = -40.6833
        station = "Cape Grim"
        
    elif file.name.startswith("best-fits_TAC"):
        # Talconeston, UK lat
        lat = 52.5127
        station = "Talconeston"
    
    else:
        raise NotImplementedError(file)

    raw = pd.read_csv(file)
    raw = raw[["Date", 'cC4F8', 'nC4F10', 'nC5F12', 
               # 'iC6F14',  # not using for now
               'nC6F14', 'nC7F16']]
    
    raw = raw.rename({
        "cC4F8": "cc4f8",
        "nC4F10": "c4f10",
        "nC5F12": "c5f12",
        "nC6F14": "c6f14",
        "nC7F16": "c7f16",
    }, axis="columns")
    raw["year"] = raw["Date"].apply(lambda x: int(x.split("/")[-1]))
    raw["month"] = raw["Date"].apply(lambda x: int(x.split("/")[1]))
    raw = raw.drop("Date", axis="columns")
    annual_mean = raw.groupby("year")[["cc4f8", "c4f10", "c5f12", "c6f14", "c7f16"]].mean()

    annual_mean.columns.name = "gas"
    annual_mean = annual_mean.stack().to_frame("value").reset_index()
    annual_mean["unit"] = "ppt"
    annual_mean["lat"] = lat
    annual_mean["station"] = station

    out_l.append(annual_mean)

clean = pd.concat(out_l)
clean

# %%
out_file = PROCESSED_DATA_DIR / "droste-et-al-2020" / "pfcs_data.csv"
out_file.parent.mkdir(exist_ok=True, parents=True)
clean.to_csv(out_file, index=False)
