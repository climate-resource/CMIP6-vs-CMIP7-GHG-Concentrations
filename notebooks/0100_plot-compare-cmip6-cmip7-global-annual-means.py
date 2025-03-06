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
# # Compare global-, annual-means

# %% [markdown]
# ## Imports

# %%
import matplotlib.pyplot as plt
import pandas_indexing as pix
import seaborn as sns
import tqdm.auto
from local.timeseries_db import get_timeseries_db

# %% [markdown]
# ## Action

# %%
db = get_timeseries_db()
db

# %%
CMIP6_SOURCE_ID = "UoM-CMIP-1-2-0"
CMIP7_SOURCE_ID = "CR-CMIP-1-0-0"

# %%
# TODO: save and then load other data sources
palette = {
    # wmo_ch7_source: "black",
    # velders_source: "tab:cyan",
    # western_source: "tab:green",
    # adam_source: "tab:green",
    CMIP6_SOURCE_ID: "tab:purple",
    CMIP7_SOURCE_ID: "tab:blue",
    # f"{droste_source}: Cape Grim": "tab:green",
    # f"{droste_source}: Talconeston": "tab:red",
}

# %%
global_annual_mean = db.load(pix.ismatch(frequency="yr", grid="gm"), progress=True)
global_annual_mean

# %%
pdf_all = global_annual_mean.melt(ignore_index=False, var_name="time").reset_index()


def get_moasic_string(inv: tuple[int, int]) -> str:
    return f"{inv[0]} - {inv[1]}"


for (gas, unit), pdf in tqdm.auto.tqdm(pdf_all.groupby(["gas", "unit"]), desc="gas"):
    mosaic = [[(1950, 2025), (1950, 2025)], [(1750, 2025), (2000, 2025)]]
    fig, axes = plt.subplot_mosaic(
        [[get_moasic_string(vv) for vv in v] for v in mosaic],
        figsize=(12, 4.5),
    )

    mosaic_unique = []
    for v in mosaic:
        for vv in v:
            if vv not in mosaic_unique:
                mosaic_unique.append(vv)

    for time_range in mosaic_unique:
        ax = axes[get_moasic_string(time_range)]
        pdf_time = pdf[(pdf["time"] >= time_range[0]) & (pdf["time"] < time_range[1])]
        sns.scatterplot(
            data=pdf_time,
            style="source_id",
            hue="source_id",
            palette=palette,
            x="time",
            y="value",
            ax=ax,
            # linewidth=2,
            alpha=0.4,
            s=75,
        )
        ax.set_ylabel(f"{gas} ({unit})")

    fig.suptitle(gas)

    plt.tight_layout()
    plt.show()

# %%
data_vars_to_plt = sorted([v for v in global_annual_mean.pix.unique("gas")])
data_vars_to_plt = ["co2"]
grid_width = 3
mosaic_data_vars = [
    [data_var for data_var in data_vars_to_plt[i : i + grid_width]]
    for i in range(0, len(data_vars_to_plt), grid_width)
]
if len(mosaic_data_vars[-1]) < grid_width:
    padding = grid_width - len(mosaic_data_vars[-1])
    mosaic_data_vars[-1].extend(padding * ["."])

mosaic_data_vars

# %%
pdf_all = (
    global_annual_mean.loc[pix.isin(gas=data_vars_to_plt)]
    .melt(ignore_index=False, var_name="time")
    .reset_index()
)

for time_range in (
    # (1980, 2005 + 1),
    # (1, 2025 + 1),
    # (1825, 1875 + 1),
    # (1750, 2025 + 1),
    # (1940, 2025 + 1),
    (1700, 1950 + 1),
    (1940, 1980 + 1),
):
    fig, axes = plt.subplot_mosaic(
        mosaic_data_vars,
        figsize=(12, 4.5 * len(mosaic_data_vars)),
    )
    for (gas, unit), pdf in tqdm.auto.tqdm(
        pdf_all.groupby(["gas", "unit"]), desc="gas", leave=False
    ):
        pdf_time = pdf[(pdf["time"] >= time_range[0]) & (pdf["time"] < time_range[1])]
        sns.scatterplot(
            data=pdf_time,
            style="source_id",
            hue="source_id",
            palette=palette,
            x="time",
            y="value",
            ax=axes[gas],
            # linewidth=2,
            alpha=0.4,
            s=75,
        )
        axes[gas].set_ylabel(f"{gas} ({unit})")

    fig.suptitle(time_range)

    plt.tight_layout()
    plt.show()
    # break

# %%
