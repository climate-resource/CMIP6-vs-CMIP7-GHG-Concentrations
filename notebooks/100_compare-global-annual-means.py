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
# # Compare global-, annual-means
#
# Here we compare the global-, annual-means for different gases.

# %%
import os
import subprocess

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import tqdm
import xarray as xr
from input4mips_validation.cvs.drs import DataReferenceSyntax

# %%
# Someone can explain a better way to do this to me another day
esgpull_config_raw = subprocess.check_output(
    ["esgpull", "config"]
).decode("utf-8")
for line in esgpull_config_raw.splitlines():
    if "data" in line:
        data_path = Path(line.split("[33m")[-2].split("\x1b")[0])
        break

else:
    msg = "Data path not found in esgpull config"
    raise AssertionError(msg)

data_path

# %%
local_data_path = (Path(".").absolute()) / ".." / ".." / "CMIP-GHG-Concentration-Generation/output-bundles/dev-test-run/data/processed/esgf-ready/input4MIPs"
local_data_path

# %%
drs_default = DataReferenceSyntax(
    directory_path_template= "<activity_id>/<mip_era>/<target_mip>/<institution_id>/<source_id>/<realm>/<frequency>/<variable_id>/<grid_label>/v<version>",
    directory_path_example= "not_used",
    filename_template="<variable_id>_<activity_id>_<dataset_category>_<target_mip>_<source_id>_<grid_label>[_<time_range>].nc",
    filename_example= "not_used",
    )
source_id_drs_map = {
    "CR-CMIP-0-3-0": drs_default,
    "CR-CMIP-testing": drs_default,
    "CR-CMIP-0-2-1a1-dev": drs_default,
    "UoM-CMIP-1-2-0": drs_default,
}
source_id_drs_map

# %%
db_l = []
for file in tqdm.tqdm([*local_data_path.rglob("**/yr/**/*gm*.nc"), *data_path.rglob("*gm*.nc"), *data_path.rglob("*gr1-GMNHSH*.nc")], desc="Extracting file metadata"):
    for source_id in source_id_drs_map:
        if source_id in str(file):
            drs = source_id_drs_map[source_id]
            break
    else:
        msg = f"No matching source ID found in {str(file)}"
        raise NotImplementedError(msg)

    metadata = (
        drs.extract_metadata_from_path(file.parent) 
        | drs.extract_metadata_from_filename(file.name) 
        | xr.open_dataset(file, decode_times=False).attrs
    )
    metadata["filepath"] = file

    db_l.append(metadata)

db = pd.DataFrame(db_l)
db

# %%
CMIP6_TO_CMIP7_VARIABLE_MAP = {'mole_fraction_of_carbon_dioxide_in_air': 'co2',
 'mole_fraction_of_methane_in_air': 'ch4',
 'mole_fraction_of_nitrous_oxide_in_air': 'n2o',
 'mole_fraction_of_c2f6_in_air': 'c2f6',
 'mole_fraction_of_c3f8_in_air': 'c3f8',
 'mole_fraction_of_c4f10_in_air': 'c4f10',
 'mole_fraction_of_c5f12_in_air': 'c5f12',
 'mole_fraction_of_c6f14_in_air': 'c6f14',
 'mole_fraction_of_c7f16_in_air': 'c7f16',
 'mole_fraction_of_c8f18_in_air': 'c8f18',
 'mole_fraction_of_c_c4f8_in_air': 'cc4f8',
 'mole_fraction_of_carbon_tetrachloride_in_air': 'ccl4',
 'mole_fraction_of_cf4_in_air': 'cf4',
 'mole_fraction_of_cfc11_in_air': 'cfc11',
 'mole_fraction_of_cfc113_in_air': 'cfc113',
 'mole_fraction_of_cfc114_in_air': 'cfc114',
 'mole_fraction_of_cfc115_in_air': 'cfc115',
 'mole_fraction_of_cfc12_in_air': 'cfc12',
 'mole_fraction_of_ch2cl2_in_air': 'ch2cl2',
 'mole_fraction_of_methyl_bromide_in_air': 'ch3br',
 'mole_fraction_of_ch3ccl3_in_air': 'ch3ccl3',
 'mole_fraction_of_methyl_chloride_in_air': 'ch3cl',
 'mole_fraction_of_chcl3_in_air': 'chcl3',
 'mole_fraction_of_halon1211_in_air': 'halon1211',
 'mole_fraction_of_halon1301_in_air': 'halon1301',
 'mole_fraction_of_halon2402_in_air': 'halon2402',
 'mole_fraction_of_hcfc141b_in_air': 'hcfc141b',
 'mole_fraction_of_hcfc142b_in_air': 'hcfc142b',
 'mole_fraction_of_hcfc22_in_air': 'hcfc22',
 'mole_fraction_of_hfc125_in_air': 'hfc125',
 'mole_fraction_of_hfc134a_in_air': 'hfc134a',
 'mole_fraction_of_hfc143a_in_air': 'hfc143a',
 'mole_fraction_of_hfc152a_in_air': 'hfc152a',
 'mole_fraction_of_hfc227ea_in_air': 'hfc227ea',
 'mole_fraction_of_hfc23_in_air': 'hfc23',
 'mole_fraction_of_hfc236fa_in_air': 'hfc236fa',
 'mole_fraction_of_hfc245fa_in_air': 'hfc245fa',
 'mole_fraction_of_hfc32_in_air': 'hfc32',
 'mole_fraction_of_hfc365mfc_in_air': 'hfc365mfc',
 'mole_fraction_of_hfc4310mee_in_air': 'hfc4310mee',
 'mole_fraction_of_nf3_in_air': 'nf3',
 'mole_fraction_of_sf6_in_air': 'sf6',
 'mole_fraction_of_so2f2_in_air': 'so2f2',
 'mole_fraction_of_cfc11eq_in_air': 'cfc11eq',
 'mole_fraction_of_cfc12eq_in_air': 'cfc12eq',
 'mole_fraction_of_hfc134aeq_in_air': 'hfc134aeq'}


# %%
def normalise_variable_names(v: str) -> str:
    if v in CMIP6_TO_CMIP7_VARIABLE_MAP:
        return CMIP6_TO_CMIP7_VARIABLE_MAP[v]

    return v


db["variable_normalised"] = db["variable_id"].apply(normalise_variable_names)
assert not [v for v in db["variable_normalised"].unique() if "mole" in v]
db


# %%
def load_cmip6_data(fp: Path) -> xr.Dataset:
    out = xr.open_dataset(fp, decode_times=False)
    
    # Drop out the first year, which is zero, and doesn't exist anywhere
    if out.attrs["frequency"] == "yr":
        out = out.isel(time=slice(1, None))
    
    else:
        out = out.isel(time=slice(12, None))
    
    if out["time"].attrs["units"] == "days since 0-1-1":
        out["time"].attrs["units"] =  "days since 0001-1-1"
        old_attrs = out["time"].attrs
        out["time"] = out["time"] - 365
        out["time"].attrs = old_attrs
    
    out = xr.decode_cf(out, decode_times=True, use_cftime=True)
    out = out.rename({k: v for k, v in CMIP6_TO_CMIP7_VARIABLE_MAP.items() if k in out.data_vars})

    return out


# %%
def load_cmip7_data(fp: Path) -> xr.Dataset:
    out = xr.open_dataset(fp, use_cftime=True)

    return out


# %%
to_load = db[db["variable_normalised"].isin([
    "cfc114",
    "hfc152a",
    "ccl4",
    # "co2", "ch4", "n2o", "cfc12", "cfc11", "cfc11eq"
])]

loaded_l = []
for _, vdf in tqdm.tqdm(to_load.groupby("variable_normalised"), desc="Variables to load"):
    variable_l = []
    for _, row in vdf.iterrows():
        fp = row["filepath"]
        source_id = row["source_id"]
        if "UoM" in source_id:
            loaded_fp = load_cmip6_data(fp)
            # We only want global-mean, hence
            loaded_fp = loaded_fp.sel(sector=0).reset_coords("sector", drop=True)
            
        else:
            loaded_fp = load_cmip7_data(fp)
    
        # Make life easy, put everything on the same calendar
        loaded_fp = loaded_fp.convert_calendar("proleptic_gregorian")
        loaded_fp = loaded_fp.assign_coords(source_id=source_id)
        variable_l.append(loaded_fp)
        
    loaded_l.append(xr.concat(variable_l, "source_id"))
        

loaded = xr.merge(loaded_l)
# Make life easy, take annual mean
loaded = loaded.groupby("time.year").mean()
loaded

# %%
for data_var in loaded.data_vars:
    if "bnds" in data_var:
        continue

    fig, axes = plt.subplot_mosaic([["recent", "recent"], ["all", "historical"]], figsize=(10, 6))

    for time_axis, ax in ((slice(None, None), "all"), (slice(1950, None), "recent"), (slice(1750, None), "historical")):
        loaded[data_var].sel(year=time_axis).plot.line(x="year", hue="source_id", linewidth=3, alpha=0.4, ax=axes[ax])

    plt.tight_layout()
    plt.show()

    
    difference = loaded[data_var].sel(source_id="CR-CMIP-0-3-0") - loaded[data_var].sel(source_id="UoM-CMIP-1-2-0")
    fig, axes = plt.subplot_mosaic([["recent", "recent"], ["all", "historical"]], figsize=(10, 6))

    for time_axis, ax in ((slice(None, None), "all"), (slice(1950, None), "recent"), (slice(1750, None), "historical")):
        difference.sel(year=time_axis).plot.line(x="year", hue="source_id", alpha=0.9, ax=axes[ax])

    plt.tight_layout()
    plt.show()
