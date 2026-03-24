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
# # Demonstrate the issue with CMIP6's equivalent concentrations

# %% [markdown]
# ## Imports

# %%
import pandas_indexing as pix
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

# %% [markdown]
# There is a clear difference in the concentrations of the equivalent species.

# %%
global_annual_mean.loc[pix.ismatch(gas="*eq"), [1.5, 1850.5, 2000.5]].unstack(
    "source_id"
)

# %% [markdown]
# This can't be explained by the difference in concentration of the underlying species.

# %%
tmp = global_annual_mean.loc[:, 1850.5].unstack("source_id")
tmp["diff"] = tmp[CMIP7_SOURCE_ID] - tmp[CMIP6_SOURCE_ID]
tmp["diff_abs"] = tmp["diff"].abs()
tmp.sort_values("diff_abs", ascending=False)

# %% [markdown]
# Hence it must come from the conversion to equivalent species.

# %% [markdown]
# The ERFs of the underlying species don't differ.

# %%
erfs = to_erf(global_annual_mean)

tmp = erfs[2005.5].unstack("source_id")
tmp["diff"] = tmp[CMIP7_SOURCE_ID] - tmp[CMIP6_SOURCE_ID]
tmp["diff_abs"] = tmp["diff"].abs()
tmp.sort_values("diff_abs", ascending=False)

# %% [markdown]
# If we sum from the raw components, we get the same answer
# for both source IDs.
# Hence the error must be in the sum of the components.

# %%
# Sum of raw components in ERF terms.
erfs_resummed = (
    erfs.loc[
        ~pix.isin(gas=["cfc11eq", "cfc12eq", "hfc134aeq", "co2", "ch4", "n2o", "cfc12"])
    ]
    .groupby(erfs.index.names.difference(["gas"]))
    .sum(min_count=2)
)
erfs_resummed

# %%
# What is reported, converted to ERF.
# Notice the clear difference from the above.
erfs.loc[pix.isin(gas="cfc11eq")]

# %%
# Also check against reported concentrations by converting back
erfs_resummed / RADIATIVE_EFFICIENCIES["cfc11"].to("W / m^2 / ppt").m

# %%
# Matches the above for CMIP7, not for CMIP6
global_annual_mean.loc[pix.isin(gas="cfc11eq")]

# %%
# There is also an issue for cfc12eq and hfc134aeq,
# which we presume has the same cause.
erfs.loc[pix.isin(gas=["cfc11eq", "cfc12eq", "hfc134aeq"])]
