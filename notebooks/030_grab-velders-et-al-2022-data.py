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
# # Grab Velders et al., 2022 data
#
# Original paper: https://doi.org/10.5194/acp-22-6087-2022
# Zenodo record: https://zenodo.org/records/6520707

# %%
import pandas as pd
import pooch

from utils import PROCESSED_DATA_DIR

# %%
raw_data_file = pooch.retrieve(
    "https://zenodo.org/records/6520707/files/veldersguus/HFC-scenarios-2022-v1.0.zip?download=1",
    known_hash="74fe066fac06b742ba4fec6ad3af52a595f81a2a1c69d53a8eaf9ca846b3a7cd",
    processor=pooch.Unzip(members=["veldersguus-HFC-scenarios-2022-859d44c/HFC_Current_Policy_2022_Scenario.xlsx"]),
)
if len(raw_data_file) != 1:
    raise AssertionError

raw_data_file = raw_data_file[0]
raw_data_file

# %%
# Doesn't matter whether we use upper or lower as we're just getting historical data
raw_excel = pd.read_excel(raw_data_file, sheet_name="Upper", header=None)
raw_excel

# %%
expected_species = ['HFC-32', 'HFC-125', 'HFC-134a', 'HFC-143a', 'HFC-152a', 'HFC-227ea',
       'HFC-236fa', 'HFC-245fa', 'HFC-365mfc', 'HFC-43-10mee']

# %%
start_idx = 4
block_length = 112
expected_n_blocks = 10

clean_l = []
for i in range(expected_n_blocks):
    start = start_idx + i * (block_length + 1)
    species_df = raw_excel.iloc[start:start + block_length]
    species_df = species_df.dropna(how="all", axis="columns")
    species_df.columns = species_df.iloc[0, :]
    species_df = species_df.iloc[1:, :]

    gas = species_df["Species"].unique()
    if len(gas) != 1:
        raise AssertionError
    gas = gas[0]

    keep = species_df[["Year", "Mix_tot"]].rename({"Year": "year", "Mix_tot": gas}, axis="columns")
    keep = keep[keep["year"] < 2025]
    keep = keep.set_index("year")
    # display(keep)

    clean_l.append(keep)

clean = pd.concat(clean_l, axis="columns")
if set(clean.columns) != set(expected_species):
    raise AssertionError
    
clean

# %%
out_file = PROCESSED_DATA_DIR / "velders-et-al-2022" / "hfc_projections.csv"
out_file.parent.mkdir(exist_ok=True, parents=True)
clean.to_csv(out_file)
