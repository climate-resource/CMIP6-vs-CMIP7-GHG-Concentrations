# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Clean CMIP6 data
#
# Load the CMIP6 data and clean it to have:
#
# - sensible variable names
# - sensible co-ordinates
#     - get rid of year 0
#     - get rid of sector
#
# Dump it out as feather files into a database.

# %%
import tqdm.auto
from local.data_reading import load_cmip6_data
from local.data_reading.cmip6 import CMIP6_TO_CMIP7_VARIABLE_MAP
from local.esgf_data_helper import DEFAULT_DRS, build_metadata_table
from local.paths import ESGF_INTAKE_DOWNLOAD_PATH
from local.time import convert_time_cols_to_plotting_float
from local.timeseries_db import get_timeseries_db

# %%
db = get_timeseries_db()
db

# %%
source_id_to_grab = "UoM-CMIP-1-2-0"

# %%
md_table = build_metadata_table(
    ESGF_INTAKE_DOWNLOAD_PATH.rglob(f"**/{source_id_to_grab}/**/*.nc"), drs=DEFAULT_DRS
)
md_table

# %%
gridded = md_table["grid_label"].isin(["gn-15x360deg"])
monthly = md_table["frequency"].isin(["mon"])

# %%
unit_map = {
    "1.e-6": "ppm",
    "1.e-9": "ppb",
    "1.e-12": "ppt",
}

gmnhsh_map = {
    "Global": "gm",
    "Northern Hemisphere": "gr1z",
    "Southern Hemisphere": "gr1z",
}

# %%
# Do fast files first
locator_pbar = tqdm.auto.tqdm(
    [
        (gridded & ~monthly, "gridded & ~monthly"),
        (~gridded & ~monthly, "~gridded & ~monthly"),
        (~gridded & monthly, "~gridded & monthly"),
        (gridded & monthly, "gridded & monthly"),
    ]
)
for locator, desc in locator_pbar:
    locator_pbar.set_description(desc)

    for (gas, frequency, grid, source_id), gdf in tqdm.auto.tqdm(
        md_table[locator].groupby(
            ["variable_id", "frequency", "grid_label", "source_id"]
        ),
        desc="gases",
        leave=False,
    ):
        gas_mapped = CMIP6_TO_CMIP7_VARIABLE_MAP[gas]

        raw = load_cmip6_data(gdf["filepath"].tolist())

        data = raw[gas_mapped]

        if "sector" in data.dims:
            sector_map = {
                int(v.split(":")[0].strip()): v.split(":")[1].strip()
                for v in data["sector"].attrs["ids"].split(";")
            }

            out = data.to_pandas().stack().unstack("time")

            out = out.reset_index()
            out["sector"] = out["sector"].map(sector_map)
            out = out.rename({"sector": "region"}, axis="columns")
            out["grid"] = out["region"].map(gmnhsh_map)

        else:
            raise NotImplementedError

        out["unit"] = unit_map[data.attrs["units"]]
        out["gas"] = gas_mapped
        out["source_id"] = source_id
        out["frequency"] = frequency
        out = out.set_index(["region", "unit", "gas", "source_id", "frequency", "grid"])

        out = convert_time_cols_to_plotting_float(out, frequency=frequency)

        db.save(
            out,
            groupby=["source_id", "gas", "frequency", "grid"],
            # progress=True,
            allow_overwrite=True,
        )
