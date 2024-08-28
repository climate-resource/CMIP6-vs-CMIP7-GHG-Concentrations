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
# # Ensure esgpull is setup
#
# This isn't actually a notebook you run here.
# Instead, open up a new terminal 
# and run the following commands.
# You should only need to do this once.
#
# ```shell
# poetry run esgpull self install
# poetry run esgpull config api.index_node esgf-node.llnl.gov
# ```
#
# It is up to you where you install esgpull.
# For most users, installing it in a default location will make sense
# because sharing your ESGF data across projects will be fine.
# For some users (e.g. those on shared systems),
# you may want to use a more specific location.
