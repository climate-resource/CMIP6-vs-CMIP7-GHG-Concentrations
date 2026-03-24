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
# # Grab CMIP6 data
#
# Here we grab the CMIP6 data we want.

# %%
CMIP6_VERSION_PROJECT = "input4MIPs"
CMIP6_VERSION_MIP_ERA = "CMIP6"
CMIP6_VERSION_SOURCE_ID = "UoM-CMIP-1-2-0"
CMIP6_VERSION_GRID = "gr1-GMNHSH"
CMIP6_VERSION_FREQUENCY = "yr"
SEARCH_TAG = f"cmip6-global-mean-yearly-{CMIP6_VERSION_SOURCE_ID.lower()}"

# %%
# !esgpull add --tag {SEARCH_TAG} --track project:{CMIP6_VERSION_PROJECT} mip_era:{CMIP6_VERSION_MIP_ERA} source_id:{CMIP6_VERSION_SOURCE_ID} grid_label:{CMIP6_VERSION_GRID} frequency:{CMIP6_VERSION_FREQUENCY}

# %%
# !esgpull update -y --tag {SEARCH_TAG}

# %%
# !esgpull download
