"""
Reading of CMIP6 data
"""

from __future__ import annotations

from pathlib import Path

import xarray as xr

CMIP6_TO_CMIP7_VARIABLE_MAP = {
    "mole_fraction_of_carbon_dioxide_in_air": "co2",
    "mole_fraction_of_methane_in_air": "ch4",
    "mole_fraction_of_nitrous_oxide_in_air": "n2o",
    "mole_fraction_of_c2f6_in_air": "c2f6",
    "mole_fraction_of_c3f8_in_air": "c3f8",
    "mole_fraction_of_c4f10_in_air": "c4f10",
    "mole_fraction_of_c5f12_in_air": "c5f12",
    "mole_fraction_of_c6f14_in_air": "c6f14",
    "mole_fraction_of_c7f16_in_air": "c7f16",
    "mole_fraction_of_c8f18_in_air": "c8f18",
    "mole_fraction_of_c_c4f8_in_air": "cc4f8",
    "mole_fraction_of_carbon_tetrachloride_in_air": "ccl4",
    "mole_fraction_of_cf4_in_air": "cf4",
    "mole_fraction_of_cfc11_in_air": "cfc11",
    "mole_fraction_of_cfc113_in_air": "cfc113",
    "mole_fraction_of_cfc114_in_air": "cfc114",
    "mole_fraction_of_cfc115_in_air": "cfc115",
    "mole_fraction_of_cfc12_in_air": "cfc12",
    "mole_fraction_of_ch2cl2_in_air": "ch2cl2",
    "mole_fraction_of_methyl_bromide_in_air": "ch3br",
    "mole_fraction_of_ch3ccl3_in_air": "ch3ccl3",
    "mole_fraction_of_methyl_chloride_in_air": "ch3cl",
    "mole_fraction_of_chcl3_in_air": "chcl3",
    "mole_fraction_of_halon1211_in_air": "halon1211",
    "mole_fraction_of_halon1301_in_air": "halon1301",
    "mole_fraction_of_halon2402_in_air": "halon2402",
    "mole_fraction_of_hcfc141b_in_air": "hcfc141b",
    "mole_fraction_of_hcfc142b_in_air": "hcfc142b",
    "mole_fraction_of_hcfc22_in_air": "hcfc22",
    "mole_fraction_of_hfc125_in_air": "hfc125",
    "mole_fraction_of_hfc134a_in_air": "hfc134a",
    "mole_fraction_of_hfc143a_in_air": "hfc143a",
    "mole_fraction_of_hfc152a_in_air": "hfc152a",
    "mole_fraction_of_hfc227ea_in_air": "hfc227ea",
    "mole_fraction_of_hfc23_in_air": "hfc23",
    "mole_fraction_of_hfc236fa_in_air": "hfc236fa",
    "mole_fraction_of_hfc245fa_in_air": "hfc245fa",
    "mole_fraction_of_hfc32_in_air": "hfc32",
    "mole_fraction_of_hfc365mfc_in_air": "hfc365mfc",
    "mole_fraction_of_hfc4310mee_in_air": "hfc4310mee",
    "mole_fraction_of_nf3_in_air": "nf3",
    "mole_fraction_of_sf6_in_air": "sf6",
    "mole_fraction_of_so2f2_in_air": "so2f2",
    "mole_fraction_of_cfc11eq_in_air": "cfc11eq",
    "mole_fraction_of_cfc12eq_in_air": "cfc12eq",
    "mole_fraction_of_hfc134aeq_in_air": "hfc134aeq",
}


def load_cmip6_data(fps: list[Path]) -> xr.Dataset:
    """
    Load CMIP6 data

    Parameters
    ----------
    fps
        File paths to load from

    Returns
    -------
    :
        Loaded dataset
    """
    out = xr.open_mfdataset(fps, decode_times=False).compute()

    # Drop out the first year, which is zero, and doesn't exist anywhere
    if out.attrs["frequency"] == "yr":
        out = out.isel(time=slice(1, None))

    else:
        out = out.isel(time=slice(12, None))

    if out["time"].attrs["units"] == "days since 0-1-1":
        out["time"].attrs["units"] = "days since 0001-1-1"
        old_attrs = out["time"].attrs
        out["time"] = out["time"] - 365
        out["time"].attrs = old_attrs

    out = xr.decode_cf(out, decode_times=True, use_cftime=True)
    out = out.rename(
        {k: v for k, v in CMIP6_TO_CMIP7_VARIABLE_MAP.items() if k in out.data_vars}
    )

    return out
