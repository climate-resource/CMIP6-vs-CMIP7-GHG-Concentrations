# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Download CMIP6 data

# %% [markdown]
# ## Imports

# %%
from intake_esgf import ESGFCatalog

# from local.paths import ESGF_INTAKE_DOWNLOAD_PATH, ESGF_INTAKE_DB_PATH

# %% [markdown]
# ## Action

# %%
# ESGFCatalog?

# %%
cat.local_cache

# %%
cat = ESGFCatalog()
cat.download_db

# %%
