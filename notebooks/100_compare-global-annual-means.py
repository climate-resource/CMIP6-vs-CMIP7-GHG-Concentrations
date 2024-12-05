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
import numpy as np
import openscm_units
import pandas as pd
import pint
import seaborn as sns
import tqdm
import xarray as xr
from input4mips_validation.cvs.drs import DataReferenceSyntax

from utils import PROCESSED_DATA_DIR, RAW_DATA_DIR

# %%
pint.set_application_registry(openscm_units.unit_registry)
Q = pint.get_application_registry().Quantity

# %% [markdown]
# # Load CMIP data

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

CMIP6_SOURCE_ID = "UoM-CMIP-1-2-0"
CMIP7_COMPARE_SOURCE_ID = "CR-CMIP-testing"
source_id_drs_map = {
    "CR-CMIP-0-3-0": drs_default,
    "CR-CMIP-testing": drs_default,
    # "CR-CMIP-0-2-1a1-dev": drs_default,
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
CMIP6_TO_CMIP7_VARIABLE_MAP = {
    'mole_fraction_of_carbon_dioxide_in_air': 'co2',
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
    'mole_fraction_of_hfc134aeq_in_air': 'hfc134aeq',
}

# %%
CMIP7_TO_NORMAL_VARIABLE_MAP = {
    'co2': 'co2',
    'ch4': 'ch4',
    'n2o': 'n2o',
    'pfc116': 'c2f6',
    'pfc218': 'c3f8',
    'pfc3110': 'c4f10',
    'pfc4112': 'c5f12',
    'pfc5114': 'c6f14',
    'pfc6116': 'c7f16',
    'pfc7118': 'c8f18',
    'pfc318': 'cc4f8',
    'ccl4': 'ccl4',
    'cf4': 'cf4',
    'cfc11': 'cfc11',
    'cfc113': 'cfc113',
    'cfc114': 'cfc114',
    'cfc115': 'cfc115',
    'cfc12': 'cfc12',
    'ch2cl2': 'ch2cl2',
    'ch3br': 'ch3br',
    'hcc140a': 'ch3ccl3',
    'ch3cl': 'ch3cl',
    'chcl3': 'chcl3',
    'halon1211': 'halon1211',
    'halon1301': 'halon1301',
    'halon2402': 'halon2402',
    'hcfc141b': 'hcfc141b',
    'hcfc142b': 'hcfc142b',
    'hcfc22': 'hcfc22',
    'hfc125': 'hfc125',
    'hfc134a': 'hfc134a',
    'hfc143a': 'hfc143a',
    'hfc152a': 'hfc152a',
    'hfc227ea': 'hfc227ea',
    'hfc23': 'hfc23',
    'hfc236fa': 'hfc236fa',
    'hfc245fa': 'hfc245fa',
    'hfc32': 'hfc32',
    'hfc365mfc': 'hfc365mfc',
    'hfc4310mee': 'hfc4310mee',
    'nf3': 'nf3',
    'sf6': 'sf6',
    'so2f2': 'so2f2',
    'cfc11eq': 'cfc11eq',
    'cfc12eq': 'cfc12eq',
    'hfc134aeq': 'hfc134aeq',
}


# %%
def normalise_variable_names(v: str) -> str:
    if v in CMIP6_TO_CMIP7_VARIABLE_MAP:
        return CMIP6_TO_CMIP7_VARIABLE_MAP[v]
        
    if v in CMIP7_TO_NORMAL_VARIABLE_MAP:
        return CMIP7_TO_NORMAL_VARIABLE_MAP[v]

    return v


db["variable_normalised"] = db["variable_id"].apply(normalise_variable_names)
assert not [v for v in db["variable_normalised"].unique() if "mole" in v]
db


# %%
def load_cmip6_data(fps: list[Path]) -> xr.Dataset:
    out = xr.open_mfdataset(fps, decode_times=False).compute()
    
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
def load_cmip7_data(fps: list[Path]) -> xr.Dataset:
    out = xr.open_mfdataset(fps, use_cftime=True).compute()

    out = out.rename({k: v for k, v in CMIP7_TO_NORMAL_VARIABLE_MAP.items() if k in out.data_vars})

    return out


# %%
to_load = db[db["variable_normalised"].isin([
    "co2", 
    "ch4", 
    "n2o",
    
    # # WMO 2022 Ch. 7 variables start
    "cfc11",
    "cfc12",
    "cfc113",
    "cfc114",
    "cfc115",
    "ccl4",
    "ch3ccl3",
    "halon1211",
    "halon1301",
    "halon2402",
    # halon 1202 not included anywhere, likely because very tiny
    "ch3br",
    "ch3cl",
    # # Western variables start
    "hcfc141b",
    "hcfc142b",
    "hcfc22",
    # Western variables end
    # WMO 2022 Ch. 7 variables end
    
    # # Velders et al., 2022 variables start
    "hfc32",
    "hfc125",
    "hfc134a",
    "hfc143a",
    "hfc152a",
    "hfc227ea",
    "hfc236fa",
    "hfc245fa",
    "hfc365mfc",
    "hfc4310mee",
    # # Velders et al., 2022 variables end

    # Equivalent species start
    "cfc11eq",
    "cfc12eq",
    "hfc134aeq",
    # Equivalent species end
    
    # Other
    "hfc23",
    "cf4",
    "c2f6",
    "c3f8",
    "c4f10",
    "c5f12",
    "c6f14",
    "c7f16",
    "c8f18",
    "cc4f8",
    "ch2cl2",
    "chcl3",
    "nf3",
    "sf6",
    "so2f2",
])]

# %%
loaded_l = []
for _, vdf in tqdm.tqdm(to_load.groupby("variable_normalised"), desc="Dataset to load"):
    variable_l = []
    for (mip_era, source_id), gdf in vdf.groupby(["mip_era", "source_id"]):
        fps = gdf["filepath"].tolist()

        if "UoM" in source_id:
            loaded_fp = load_cmip6_data(fps)
            # We only want global-mean, hence
            loaded_fp = loaded_fp.sel(sector=0).reset_coords("sector", drop=True)
            
        else:
            loaded_fp = load_cmip7_data(fps)
    
        # Make life easy, put everything on the same calendar
        loaded_fp = loaded_fp.convert_calendar("proleptic_gregorian")
        loaded_fp = loaded_fp.assign_coords(source_id=source_id)
        variable_l.append(loaded_fp)
        
    loaded_l.append(xr.concat(variable_l, "source_id", combine_attrs="drop_conflicts"))
        
loaded = xr.merge(loaded_l, combine_attrs="drop_conflicts")
# Make life easy, take annual mean
loaded = loaded.groupby("time.year").mean()
loaded

# %% [markdown]
# ## Load WMO 2022 ozone assessment Chapter 7 data

# %%
WMO_CH7_DATA_PATH = RAW_DATA_DIR / "wmo-2022" / "wmo2022_Ch7_mixingratios.xlsx"

# %%
# Created with:
# `# {k: k.lower().replace("-", "") for k in wmo_ch7_df.columns}`
wmo_variable_normalisation_map = {
    'CFC-11': 'cfc11',
    'CFC-12': 'cfc12',
    'CFC-113': 'cfc113',
    'CFC-114': 'cfc114',
    'CFC-115': 'cfc115',
    'CCl4': 'ccl4',
    'CH3CCl3': 'ch3ccl3',
    'HCFC-22': 'hcfc22',
    'HCFC-141b': 'hcfc141b',
    'HCFC-142b': 'hcfc142b',
    'halon-1211': 'halon1211',
    'halon-1202': 'halon1202',
    'halon-1301': 'halon1301',
    'halon-2402': 'halon2402',
    'CH3Br': 'ch3br',
    'CH3Cl': 'ch3cl',
}

# %%
wmo_ch7_source = "WMO 2022 Ch. 7"
wmo_ch7_df_raw = pd.read_excel(WMO_CH7_DATA_PATH)
wmo_ch7_df = wmo_ch7_df_raw.rename({"Year": "year", **wmo_variable_normalisation_map}, axis="columns")
wmo_ch7_df["source"] = wmo_ch7_source

# WMO data is start of year, yet we want mid-year values, hence do the below
wmo_ch7_df = wmo_ch7_df.set_index(["year", "source"])
tmp = (wmo_ch7_df.iloc[:-1, :].values + wmo_ch7_df.iloc[1:, :].values) / 2.0
wmo_ch7_df = wmo_ch7_df.iloc[:-1, :]
wmo_ch7_df.iloc[:, :] = tmp
wmo_ch7_df = wmo_ch7_df.reset_index()

wmo_ch7_df

# %% [markdown]
# ## Load Western et al. 2024 data

# %%
wesetern_variable_normalisation_map = {
    'HCFC-22': 'hcfc22',
    'HCFC-141b': 'hcfc141b',
    'HCFC-142b': 'hcfc142b',
}

# %%
western_source = "Western et al., 2024"
western_df_raw = pd.read_csv(PROCESSED_DATA_DIR / "western-et-al-2024" / "hcfc_projections.csv")
western_df = western_df_raw.rename({"Year": "year", **wesetern_variable_normalisation_map}, axis="columns")
western_df["source"] = western_source

# Western data is start of year, yet we want mid-year values, hence do the below
western_df = western_df.set_index(["year", "source"])
tmp = (western_df.iloc[:-1, :].values + western_df.iloc[1:, :].values) / 2.0
western_df = western_df.iloc[:-1, :]
western_df.iloc[:, :] = tmp
western_df = western_df.reset_index()

western_df

# %% [markdown]
# ## Load Velders et al. 2022 data

# %%
velders_variable_normalisation_map = {
    'HFC-32': 'hfc32',
    'HFC-125': 'hfc125',
    'HFC-134a': 'hfc134a',
    'HFC-143a': 'hfc143a',
    'HFC-152a': 'hfc152a',
    'HFC-227ea': 'hfc227ea',
    'HFC-236fa': 'hfc236fa',
    'HFC-245fa': 'hfc245fa',
    'HFC-365mfc': 'hfc365mfc',
    'HFC-43-10mee': 'hfc4310mee',
}

# %%
velders_source = "Velders et al., 2022"
velders_df_raw = pd.read_csv(PROCESSED_DATA_DIR / "velders-et-al-2022" / "hfc_projections.csv")
velders_df = velders_df_raw.rename({"Year": "year", **velders_variable_normalisation_map}, axis="columns")
velders_df["source"] = velders_source

# Velders data is start of year, yet we want mid-year values, hence do the below
velders_df = velders_df.set_index(["year", "source"])
tmp = (velders_df.iloc[:-1, :].values + velders_df.iloc[1:, :].values) / 2.0
velders_df = velders_df.iloc[:-1, :]
velders_df.iloc[:, :] = tmp
velders_df = velders_df.reset_index()

# # While waiting for Guus' update
# velders_df_raw = pd.read_csv(PROCESSED_DATA_DIR / ".." / ".." / ".." / "CMIP-GHG-Concentration-Generation" / "output-bundles/dev-test-run/data/interim/velders-et-al-2022/velders_et_al_2022.csv")
# velders_df = velders_df_raw.pivot(columns="gas", index="year", values="value").reset_index()
# velders_df["source"] = velders_source

velders_df

# %% [markdown]
# ## Load Droste et al. 2020 data

# %%
droste_source = "Droste et al., 2020"

def to_plotable_droste(idf: pd.DataFrame) -> pd.DataFrame:
    out = idf.pivot(columns="gas", index="year", values="value").reset_index()
    station = idf["station"].unique()
    if len(station) > 1:
        raise AssertionError

    station = station[0]
    out["source"] = f"{droste_source}: {station}"

    return out


# %%
droste_df_raw = pd.read_csv(PROCESSED_DATA_DIR / "droste-et-al-2020" / "pfcs_data.csv")
droste_df = droste_df_raw.copy()

droste_df_cg = to_plotable_droste(droste_df[droste_df["station"] == "Cape Grim"])
droste_df_tal = to_plotable_droste(droste_df[droste_df["station"] == "Talconeston"])

droste_df_tal

# %% [markdown]
# ## Plot

# %% [markdown]
# ### Against other data sources

# %%
data_vars_to_plt = sorted([v for v in loaded.data_vars if "bnds" not in v])
grid_width = 3
mosaic_data_vars = [
    [
        data_var
        for data_var in data_vars_to_plt[i : i + grid_width]
    ]
    for i in range(0, len(data_vars_to_plt), grid_width)
]
if len(mosaic_data_vars[-1]) < grid_width:
    padding = grid_width - len(mosaic_data_vars[-1])
    mosaic_data_vars[-1].extend(padding * [""])
    
mosaic_data_vars

# %%
palette = {
    wmo_ch7_source: "black",
    velders_source: "tab:cyan",
    western_source: "tab:green",
    CMIP6_SOURCE_ID: "tab:purple",
    CMIP7_COMPARE_SOURCE_ID: "tab:red",
    f"{droste_source}: Cape Grim": "tab:green",
    f"{droste_source}: Talconeston": "tab:red",
    "CR-CMIP-0-3-0": "tab:gray",
}

# %%
for time_range in (
    range(1940, 2025 + 1),
    range(2000, 2025 + 1),
    range(1750, 2025 + 1),
):
    fig, axes = plt.subplot_mosaic(
        mosaic_data_vars,
        figsize=(12, 4.5 * len(mosaic_data_vars)),
    )

    for data_var in data_vars_to_plt:
        cmip_data = loaded[data_var].to_dataframe().reset_index().rename({"source_id": "source"}, axis="columns")

        pdf = cmip_data.copy()
        
        if data_var in wmo_ch7_df:
            pdf = pd.concat([pdf, wmo_ch7_df[["year", "source", data_var]]]).reset_index(drop=True)
        else:
            print(f"{data_var} not in WMO 2022 Ch. 7")
            
        if data_var in western_df:
            pdf = pd.concat([pdf, western_df[["year", "source", data_var]]]).reset_index(drop=True)
        else:
            print(f"{data_var} not in Western et al., 2024")
            
        if data_var in velders_df:
            pdf = pd.concat([pdf, velders_df[["year", "source", data_var]]]).reset_index(drop=True)
        else:
            print(f"{data_var} not in Velders et al., 2022")
            
        if data_var in droste_df_cg:
            pdf = pd.concat([pdf, droste_df_cg[["year", "source", data_var]]]).reset_index(drop=True)
        else:
            print(f"{data_var} not in Droste et al., 2022, Cape Grim")
            
        if data_var in droste_df_tal:
            pdf = pd.concat([pdf, droste_df_tal[["year", "source", data_var]]]).reset_index(drop=True)
        else:
            print(f"{data_var} not in Droste et al., 2022, Tacloneston")

         
        
        pdf = pdf[pdf["year"].isin(time_range)]
        
        sns.scatterplot(
            data=pdf,
            style="source",
            hue="source",
            palette=palette,
            x="year",
            y=data_var,
            ax=axes[data_var],
            # linewidth=2, 
            alpha=0.4,
            s=75,
        )

        axes[data_var].axhline(0, linestyle="--", color="k")
        
    fig.suptitle(time_range)
    
    plt.tight_layout()

    fig.savefig(f"comparison_{time_range[0]}-{time_range[-1]}.pdf")
    plt.show()

# %%
print("done")

# %% [markdown]
# ### Changes since CMIP6

# %%
# Table 7.SM.6 of https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter07_SM.pdf
RADIATIVE_EFFICIENCIES: dict[str, pint.UnitRegistry.Quantity] = {
    "co2": Q(1.33e-5, "W / m^2 / ppb"),
    "ch4": Q(0.000388, "W / m^2 / ppb"),
    "n2o": Q(0.0032, "W / m^2 / ppb"),
    # Chlorofluorocarbons
    "cfc11": Q(0.291, "W / m^2 / ppb"),
    "cfc11eq": Q(0.291, "W / m^2 / ppb"),
    "cfc12": Q(0.358, "W / m^2 / ppb"),
    "cfc12eq": Q(0.358, "W / m^2 / ppb"),
    "cfc113": Q(0.301, "W / m^2 / ppb"),
    "cfc114": Q(0.314, "W / m^2 / ppb"),
    "cfc115": Q(0.246, "W / m^2 / ppb"),
    # Hydrofluorochlorocarbons
    "hcfc22": Q(0.214, "W / m^2 / ppb"),
    "hcfc141b": Q(0.161, "W / m^2 / ppb"),
    "hcfc142b": Q(0.193, "W / m^2 / ppb"),
    # Hydrofluorocarbons
    "hfc23": Q(0.191, "W / m^2 / ppb"),
    "hfc32": Q(0.111, "W / m^2 / ppb"),
    "hfc125": Q(0.234, "W / m^2 / ppb"),
    "hfc134a": Q(0.167, "W / m^2 / ppb"),
    "hfc134aeq": Q(0.167, "W / m^2 / ppb"),
    "hfc143a": Q(0.168, "W / m^2 / ppb"),
    "hfc152a": Q(0.102, "W / m^2 / ppb"),
    "hfc227ea": Q(0.273, "W / m^2 / ppb"),
    "hfc236fa": Q(0.251, "W / m^2 / ppb"),
    "hfc245fa": Q(0.245, "W / m^2 / ppb"),
    "hfc365mfc": Q(0.228, "W / m^2 / ppb"),
    "hfc4310mee": Q(0.357, "W / m^2 / ppb"),
    # Chlorocarbons and Hydrochlorocarbons
    "ch3ccl3": Q(0.065, "W / m^2 / ppb"),
    "ccl4": Q(0.166, "W / m^2 / ppb"),
    "ch3cl": Q(0.005, "W / m^2 / ppb"),
    "ch2cl2": Q(0.029, "W / m^2 / ppb"),
    "chcl3": Q(0.074, "W / m^2 / ppb"),
    # Bromocarbons, Hydrobromocarbons and Halons
    "ch3br": Q(0.004, "W / m^2 / ppb"),
    "halon1211": Q(0.300, "W / m^2 / ppb"),
    "halon1301": Q(0.299, "W / m^2 / ppb"),
    "halon2402": Q(0.312, "W / m^2 / ppb"),
    # Fully Fluorinated Species
    "nf3": Q(0.204, "W / m^2 / ppb"),
    "sf6": Q(0.567, "W / m^2 / ppb"),
    "so2f2": Q(0.211, "W / m^2 / ppb"),
    "cf4": Q(0.099, "W / m^2 / ppb"),
    "c2f6": Q(0.261, "W / m^2 / ppb"),
    "c3f8": Q(0.270, "W / m^2 / ppb"),
    "cc4f8": Q(0.314, "W / m^2 / ppb"),
    "c4f10": Q(0.369, "W / m^2 / ppb"),
    "c5f12": Q(0.408, "W / m^2 / ppb"),
    "c6f14": Q(0.449, "W / m^2 / ppb"),
    "c7f16": Q(0.503, "W / m^2 / ppb"),
    "c8f18": Q(0.558, "W / m^2 / ppb"),    
}

rad_eff_match_units = {}
for k, v in RADIATIVE_EFFICIENCIES.items():
    if k in ["co2"]:
        rad_eff_match_units[k] = v.to("W / m^2 / ppm")
    elif k in ["ch4", "n2o"]:
        rad_eff_match_units[k] = v.to("W / m^2 / ppb")
    else:
        rad_eff_match_units[k] = v.to("W / m^2 / ppt")
        
rad_eff_match_units

# %%
for data_var in sorted(loaded.data_vars):
# for data_var in ["co2", "ch4", "n2o", "cfc11eq", "cfc12eq", "hfc134aeq", "cfc11", "cfc12", "hfc134a"]:
    if "bnds" in data_var:
        continue

    parray = loaded[data_var].dropna("source_id", how="all")
    
    if parray.sel(year=range(1900, 2010 + 1)).isnull().sum() > 0:
        msg = f"Likely renaming error for {data_var}"
        raise AssertionError(msg)

    difference = parray.sel(source_id=CMIP7_COMPARE_SOURCE_ID) - parray.sel(source_id=CMIP6_SOURCE_ID)
    difference_erf = difference * rad_eff_match_units[difference.name]

    difference_erf_max = difference_erf.max().data
    if difference_erf_max.m > 0.01:  # "W / m^2"
        print("!!! Look here !!!")
    print(f"{data_var}: {difference_erf_max=:.3e}")
    print()

# %%
for data_var in sorted(loaded.data_vars):
# for data_var in ["co2", "ch4", "n2o", "cfc11eq", "cfc12eq", "hfc134aeq", "cfc11", "cfc12", "hfc134a"]:
    if "bnds" in data_var:
        continue

    parray = loaded[data_var].dropna("source_id", how="all")
    
    if parray.sel(year=range(1900, 2010 + 1)).isnull().sum() > 0:
        msg = f"Likely renaming error for {data_var}"
        raise AssertionError(msg)

    fig, axes = plt.subplot_mosaic([["recent", "recent"], ["all", "historical"]], figsize=(10, 6))

    for time_axis, ax in ((slice(None, None), "all"), (slice(1950, None), "recent"), (slice(1750, None), "historical")):
        parray.sel(year=time_axis).plot.line(x="year", hue="source_id", linewidth=3, alpha=0.4, ax=axes[ax])

    fig.suptitle(parray.name)
    
    plt.tight_layout()
    plt.show()

    difference = parray.sel(source_id=CMIP7_COMPARE_SOURCE_ID) - parray.sel(source_id=CMIP6_SOURCE_ID)

    try:
        difference_rf = difference * rad_eff_match_units[difference.name]
            
        fig, axes = plt.subplot_mosaic([["recent", "recent"], ["all", "historical"]], figsize=(10, 6))
    
        for time_axis, ax in ((slice(None, None), "all"), (slice(1950, None), "recent"), (slice(1750, None), "historical")):
            difference_rf.sel(year=time_axis).plot.line(x="year", hue="source_id", alpha=0.9, ax=axes[ax])
    
        fig.suptitle(f"{parray.name} ERF difference ({CMIP7_COMPARE_SOURCE_ID} - {CMIP6_SOURCE_ID})")
        
        plt.tight_layout()
        plt.show()
    except KeyError:
        print(f"No radiative efficiency for {data_var}")
        
    fig, axes = plt.subplot_mosaic([["recent", "recent"], ["all", "historical"]], figsize=(10, 6))

    for time_axis, ax in ((slice(None, None), "all"), (slice(1950, None), "recent"), (slice(1750, None), "historical")):
        difference.sel(year=time_axis).plot.line(x="year", hue="source_id", alpha=0.9, ax=axes[ax])

    fig.suptitle(f"{parray.name} absolute difference ({CMIP7_COMPARE_SOURCE_ID} - {CMIP6_SOURCE_ID})")
    
    plt.tight_layout()
    plt.show()
    
    difference_rel = (parray.sel(source_id=CMIP7_COMPARE_SOURCE_ID) - parray.sel(source_id=CMIP6_SOURCE_ID)) / parray.sel(source_id=CMIP7_COMPARE_SOURCE_ID) * 100
    fig, axes = plt.subplot_mosaic([["recent", "recent"], ["all", "historical"]], figsize=(10, 6))

    for time_axis, ax in ((slice(None, None), "all"), (slice(1950, None), "recent"), (slice(1750, None), "historical")):
        difference_rel.sel(year=time_axis).plot.line(x="year", hue="source_id", alpha=0.9, ax=axes[ax])

    fig.suptitle(f"{parray.name} percentage difference ({CMIP7_COMPARE_SOURCE_ID} - {CMIP6_SOURCE_ID})")
    
    plt.tight_layout()
    plt.show()

    # break
