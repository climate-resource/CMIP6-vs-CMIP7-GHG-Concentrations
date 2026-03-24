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
# # Plot in concentration terms

# %% [markdown]
# ## Imports

# %%
import matplotlib.pyplot as plt
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
global_annual_mean = global_annual_mean.pix.assign(
    mip_era=global_annual_mean.index.get_level_values("source_id").map(
        {CMIP6_SOURCE_ID: "CMIP6", CMIP7_SOURCE_ID: "CMIP7"}
    )
)
global_annual_mean

# %%
pdf = (
    global_annual_mean.loc[
        pix.isin(gas=["total", "co2", "ch4", "n2o", "cfc12eq", "hfc134aeq"]), 1750:
    ]
    .melt(ignore_index=False, var_name="time")
    .reset_index()
)

fg = sns.relplot(
    data=pdf,
    x="time",
    y="value",
    hue="mip_era",
    col="gas",
    col_wrap=3,
    kind="line",
    # palette={
    #     "total": "black",
    #     "co2": "tab:blue",
    #     "ch4": "tab:red",
    #     "n2o": "tab:green",
    #     "cfc12": "tab:purple",
    #     "cfc11": "tab:olive",
    #     "cfc12eq": "tab:purple",
    #     "hfc134aeq": "tab:olive",
    # },
    alpha=0.7,
    linewidth=3,
    facet_kws=dict(sharey=False),
)
# ax.set_title("CMIP7 ERF (approx. as linearised)")
# ax.set_ylabel("W / m^2")
# ax.legend(loc="center left", bbox_to_anchor=(1.05, 0.5))

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
ax = (
    erf_total.subtract(erf_total[1750.5], axis="rows")
    .pix.project("mip_era")
    .T.loc[1750:2023]
    .plot(linewidth=3, alpha=0.5)
)
ax.set_title("Approx. (linearised) total GHG ERF")
ax.set_ylabel("W  / m^2")

# %%
erf_total_diff = (
    erf_total.reset_index("mip_era", drop=True).stack().unstack("source_id")
)
erf_total_diff = erf_total_diff[CMIP7_SOURCE_ID] - erf_total_diff[CMIP6_SOURCE_ID]
erf_total_diff = erf_total_diff.unstack().pix.assign(mip_era="CMIP7 - CMIP6")
# erf_total_diff.abs().pix.project("mip_era").T.sort_values("CMIP7 - CMIP6", axis=0, ascending=False).iloc[:30, :]

for time_min in [1, 1750]:
    ax = erf_total_diff.pix.project("mip_era").T.loc[time_min:].plot()
    ax.set_title("Approx. (linearised) change in total GHG ERF")
    ax.set_ylabel("W  / m^2")
    plt.show()

# erf_total_diff.max(axis="columns")
# erf_total_diff.idxmax(axis="columns")

# %%
erfs_diff = erfs.reset_index("mip_era", drop=True).stack().unstack("source_id")
erfs_diff = erfs_diff[CMIP7_SOURCE_ID] - erfs_diff[CMIP6_SOURCE_ID]
erfs_diff = erfs_diff.unstack().pix.assign(mip_era="CMIP7 - CMIP6")
erfs_diff = pix.concat([erfs_diff, erf_total_diff])
erfs_diff

# %%
pdf = (
    erfs_diff.loc[
        pix.isin(gas=["total", "co2", "ch4", "n2o", "cfc12eq", "hfc134aeq"]), 1750:
    ]
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
        "cfc12eq": "tab:purple",
        "hfc134aeq": "tab:olive",
    },
    alpha=0.7,
    linewidth=2,
)
ax.set_title("Difference (CMIP7 - CMIP6)\nin radiative forcing (approx. as linearised)")
ax.set_ylabel("W / m^2")
ax.legend(loc="center left", bbox_to_anchor=(1.05, 0.5))
# Notes:
# - CO2 change from updated ice cores, more obs and better use of Scripps
# - N2O change from updated ice cores
# - CH4 change from updated processing

# %%
# pdf = (
#     erfs_diff.loc[pix.ismatch(gas="*eq"), 1850:]
#     .melt(ignore_index=False, var_name="time")
#     .reset_index()
# )

# ax = sns.lineplot(
#     data=pdf,
#     x="time",
#     y="value",
#     hue="gas",
#     alpha=0.7,
#     linewidth=2,
# )
# ax.set_title("Difference (CMIP7 - CMIP6)\nin radiative forcing (approx. as linearised)")
# # Notes: issues with equivalence identified elsewhere

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
pdf = (
    erf_true.loc[
        pix.isin(
            gas=["total", "co2", "ch4", "n2o", "cfc12eq", "hfc134aeq"],
            mip_era=["CMIP7"],
        ),
        1750:,
    ]
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
        "cfc12eq": "tab:purple",
        "hfc134aeq": "tab:olive",
    },
    alpha=0.7,
    linewidth=3,
)
ax.set_title("CMIP7 ERF (approx. as linearised)")
ax.set_ylabel("W / m^2")
# ax.legend(loc="center left", bbox_to_anchor=(1.05, 0.5))

# %%
gas_order = ["co2", "ch4", "n2o", "cfc12eq", "hfc134aeq"]
ax = (
    erf_true.loc[pix.isin(source_id=CMIP7_SOURCE_ID, gas=gas_order)]
    .pix.project("gas")
    .T.loc[1750:, gas_order]
    .plot.area()
)
ax.set_title("Approximate ERF contributions")
