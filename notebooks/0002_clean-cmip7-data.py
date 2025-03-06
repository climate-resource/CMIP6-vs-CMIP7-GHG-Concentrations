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
# # Clean CMIP7 data
#
# Load the CMIP7 data and clean it into our database.

# %% [markdown]
# # Imports

# %%
import tqdm.auto
import xarray as xr
from local.esgf_data_helper import DEFAULT_DRS, build_metadata_table
from local.paths import ESGF_INTAKE_DOWNLOAD_PATH
from local.time import convert_time_cols_to_plotting_float
from local.timeseries_db import get_timeseries_db

# %% [markdown]
# ## Action

# %%
db = get_timeseries_db()
db

# %%
source_id_to_grab = "CR-CMIP-1-0-0"

# %%
md_table = build_metadata_table(
    ESGF_INTAKE_DOWNLOAD_PATH.rglob(f"**/{source_id_to_grab}/**/*.nc"), drs=DEFAULT_DRS
)
md_table

# %%
gridded = md_table["grid_label"].isin(["gnz"])
monthly = md_table["frequency"].isin(["mon"])

# %%
# unit_map = {
#     "1.e-6": "ppm",
#     "1.e-9": "ppb",
#     "1.e-12": "ppt",
# }

# gmnhsh_map = {
#     "Global": "gm",
#     "Northern Hemisphere": "gr1z",
#     "Southern Hemisphere": "gr1z",
# }

# %%
# Do fast files first
locator_pbar = tqdm.auto.tqdm(
    [
        (~gridded & ~monthly, "~gridded & ~monthly"),
        (gridded & ~monthly, "gridded & ~monthly"),
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
        raw = xr.open_mfdataset(
            gdf["filepath"].tolist(),
            decode_times=xr.coders.CFDatetimeCoder(use_cftime=True),
        )

        data = raw[gas]

        if len(data.dims) == 1:
            out = data.to_pandas().to_frame().T
            out.index.name = "gas"
            out.columns = out.columns.tolist()
            out["region"] = "Global"

        else:
            out = data.to_pandas().stack().unstack("time")
            out.columns = out.columns.tolist()
            out["gas"] = gas
            if len(out.index) == 2:
                out["region"] = out.index.map(
                    {-45.0: "Southern Hemisphere", 45.0: "Northern Hemisphere"}
                )

        out["unit"] = data.attrs["units"]
        out["grid"] = grid
        out["source_id"] = source_id
        out["frequency"] = frequency
        out_index = ["unit", "source_id", "frequency", "grid"]
        if "region" in out:
            out_index.append("region")
        if "gas" in out:
            out_index.append("gas")

        out = out.set_index(out_index, append=True)

        out = convert_time_cols_to_plotting_float(out, frequency=frequency)

        db.save(
            out,
            groupby=["source_id", "gas", "frequency", "grid"],
            # progress=True,
            allow_overwrite=True,
        )

    #     break
    # break
