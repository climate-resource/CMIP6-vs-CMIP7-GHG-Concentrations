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
# # Download ESGF data
#
# Download data from ESGF using [intake-esgf](https://intake-esgf.readthedocs.io/en/latest/beginner.html).
#
# Having now tried this and
# [esgpull](https://esgf.github.io/esgf-download),
# there is no ideal solution.
#
# Issues:
#
# - esgpull: downloads to the same location in every project,
#   so there's no way to isolate/update and doesn't give
#   any control over which node to download from
# - intake-esgf: downloads but no way to load from local paths
#   without searching first, doesn't download to a temporary
#   file so if the search is interrupted, your database is broken.
#   Also doesn't support input4MIPs.
# - neither of them support retries, which you have to have with ESGF

# %% [markdown]
# ## Imports

# %%
from intake_esgf import ESGFCatalog
from local.intake_esgf_helper import set_intake_esgf_conf_defaults

# %%
set_intake_esgf_conf_defaults()

# %% [markdown]
# ## Action

# %%
cat = ESGFCatalog()
# cat

# %%
# Monkey patch in input4MIPs support
import intake_esgf.projects
from intake_esgf.exceptions import ProjectHasNoFacet


class input4MIPs(
    intake_esgf.projects.ESGFProject
):  # Downscaled Regional Climate Data Product
    def __init__(self):
        self.facets = [
            "activity_id",
            "mip_era",
            "target_mip",
            "institution_id",
            "source_id",
            "realm",
            "frequency",
            "variable_id",
            "grid_label",
            "version",
            "data_node",
        ]

    def master_id_facets(self) -> list[str]:
        # input4MIPs.CMIP6.CMIP.UoM.UoM-CMIP-1-2-0.atmos.mon.mole-fraction-of-hfc134aeq-in-air.gr-0p5x360deg
        return [
            "activity_id",
            "mip_era",
            "target_mip",
            "institution_id",
            "source_id",
            "realm",
            "frequency",
            "variable_id",
            "grid_label",
        ]

    def id_facets(self) -> list[str]:
        # input4MIPs.CMIP6.CMIP.UoM.UoM-CMIP-1-2-0.atmos.mon.mole-fraction-of-hfc134aeq-in-air.gr-0p5x360deg.v20160830|aims3.llnl.gov
        return [
            "activity_id",
            "mip_era",
            "target_mip",
            "institution_id",
            "source_id",
            "realm",
            "frequency",
            "variable_id",
            "grid_label",
            "version",
            "data_node",
        ]

    def relaxation_facets(self) -> list[str]:
        # NOTE: This is used to find cell measures that are closely related to a given
        # set of facets and in this project do not make sense.
        return ["realm"]

    def variable_description_facets(self) -> list[str]:
        return ["variable_id"]

    def variable_facet(self) -> str:
        return "variable_id"

    def model_facet(self) -> str:
        return ProjectHasNoFacet("input4mips", "model")
        # # Near enough
        # return "source_id"

    def variant_facet(self) -> str:
        raise ProjectHasNoFacet("input4mips", "variant")

    def grid_facet(self) -> str:
        return "grid_label"


intake_esgf.projects.projects["input4mips"] = input4MIPs()

# %%
# The LLNL node really can't handle more than this for some reason
intake_esgf.conf.set(num_threads=2)

# %%
# For some reason the system cannot handle downloading
# both mon and yr at once
# or the different grids at once
for source_id, grid, frequency in (
    ("CR-CMIP-1-0-0", "gm", "yr"),
    ("CR-CMIP-1-0-0", "gm", "mon"),
    ("CR-CMIP-1-0-0", "gr1z", "yr"),
    ("CR-CMIP-1-0-0", "gr1z", "mon"),
    ("CR-CMIP-1-0-0", "gnz", "mon"),
    ("UoM-CMIP-1-2-0", "gr1-GMNHSH", "yr"),
    ("UoM-CMIP-1-2-0", "gr1-GMNHSH", "mon"),
    ("UoM-CMIP-1-2-0", "gn-15x360deg", "mon"),
):
    search_res = cat.search(
        project="input4MIPs",
        source_id=source_id,
        grid_label=grid,
        frequency=frequency,
    )

    # This triggers the download
    paths = search_res.to_path_dict()
    msg = f"{source_id} {grid} {frequency} {len(paths)} paths/datasets"
    print(msg)
