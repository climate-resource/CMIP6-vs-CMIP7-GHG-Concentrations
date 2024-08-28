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
# # Grab CMIP7 data
#
# Here we grab the CMIP7 data we want.

# %%
# Will switch to CMIP7 at some point
CMIP7_VERSION_PROJECT = "input4MIPs"
CMIP7_VERSION_MIP_ERA = "CMIP6Plus"
CMIP7_VERSION_SOURCE_ID = "CR-CMIP-0-3-0"
CMIP7_VERSION_GRID = "gm"
CMIP7_VERSION_FREQUENCY = "yr"
SEARCH_TAG = "cmip7-global-mean-yearly"

# %%
# !esgpull add --tag {SEARCH_TAG} --track project:{CMIP7_VERSION_PROJECT} mip_era:{CMIP7_VERSION_MIP_ERA} source_id:{CMIP7_VERSION_SOURCE_ID} grid_label:{CMIP7_VERSION_GRID} frequency:{CMIP7_VERSION_FREQUENCY}

# %%
# !esgpull update -y --tag {SEARCH_TAG}

# %%
# !esgpull download
