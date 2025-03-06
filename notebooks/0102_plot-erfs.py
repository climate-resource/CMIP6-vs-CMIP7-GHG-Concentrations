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
# # Plot in ERF terms

# %% [markdown]
# ## Imports

# %%
import pandas_indexing as pix
import seaborn as sns
from local.erf import RADIATIVE_EFFICIENCIES, to_erf
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
global_annual_mean = db.load(
    pix.ismatch(frequency="yr", grid="gm"), progress=True
).reset_index("lat", drop=True)
global_annual_mean

# %%
erfs = to_erf(global_annual_mean)

# %%
erf_total = (
    erfs.loc[~pix.ismatch(gas="*eq")]
    .groupby(erfs.index.names.difference(["gas"]))
    .sum(min_count=1)
    .pix.assign(gas="total")
)
erf_total

# %%
# Not really ERF
erf_total.pix.project("source_id").T.loc[1750:2023].plot()

# %%
erf_total_diff = erf_total.stack().unstack("source_id")
erf_total_diff = erf_total_diff[CMIP7_SOURCE_ID] - erf_total_diff[CMIP6_SOURCE_ID]
erf_total_diff = erf_total_diff
erf_total_diff.unstack().T.loc[1750:].plot()
# erf_total_diff

# %%
erfs_diff = erfs.stack().unstack("source_id")
erfs_diff = erfs_diff[CMIP7_SOURCE_ID] - erfs_diff[CMIP6_SOURCE_ID]
erfs_diff = pix.concat([erfs_diff, erf_total_diff]).unstack()
erfs_diff

# %%
pdf = (
    erfs_diff.loc[pix.isin(gas=["total", "co2", "ch4", "n2o", "cfc11", "cfc12"]), 1850:]
    .melt(ignore_index=False, var_name="time")
    .reset_index()
)

ax = sns.lineplot(
    data=pdf,
    x="time",
    y="value",
    hue="gas",
    palette={
        "total": "black",
        "co2": "tab:blue",
        "ch4": "tab:red",
        "n2o": "tab:green",
        "cfc12": "tab:purple",
        "cfc11": "tab:olive",
    },
    alpha=0.7,
    linewidth=2,
)
ax.set_title("Difference (CMIP7 - CMIP6)\nin radiative forcing (approx. as linearised)")
# Notes:
# - CO2 change from updated ice cores, more obs and better use of Scripps
# - N2O change from updated ice cores
# - CH4 change from updated processing

# %%
pdf = (
    erfs_diff.loc[pix.ismatch(gas="*eq"), 1850:]
    .melt(ignore_index=False, var_name="time")
    .reset_index()
)

ax = sns.lineplot(
    data=pdf,
    x="time",
    y="value",
    hue="gas",
    alpha=0.7,
    linewidth=2,
)
ax.set_title("Difference (CMIP7 - CMIP6)\nin radiative forcing (approx. as linearised)")
# Notes: issues with equivalence identified elsewhere

# %%
# More like an ERF
erf_total.subtract(erf_total[1750.5], axis="rows").pix.project("source_id").T.loc[
    1750:2023
].plot()

# %%
co2_eq_unit = "ppm"
co2_approx_var = "co2_eq_approx_marginal"
(
    erf_total.subtract(erf_total[1750.5], axis="rows")
    / RADIATIVE_EFFICIENCIES["co2"].to(f"W / m^2 / {co2_eq_unit}").m
).pix.assign(unit=co2_eq_unit, gas=co2_approx_var).add(
    global_annual_mean.loc[pix.ismatch(gas="co2")][1850.5].pix.assign(
        gas=co2_approx_var
    ),
    axis="rows",
).loc[:, 1750:]

# %%
erf_true = erfs.subtract(erfs[1750.5], axis="rows")
erf_true

# %%
gas_order = ["co2", "ch4", "n2o", "cfc12", "cfc11eq"]
ax = (
    erf_true.loc[pix.isin(source_id=CMIP7_SOURCE_ID, gas=gas_order)]
    .pix.project("gas")
    .T.loc[1750:, gas_order]
    .plot.area()
)
ax.set_title("Approximate ERF contributions")
