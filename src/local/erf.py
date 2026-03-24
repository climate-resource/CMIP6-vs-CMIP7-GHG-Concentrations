"""
Conversion to ERF
"""

from __future__ import annotations

import pandas as pd
import pint
from openscm_units import unit_registry as UR

Q = UR.Quantity

# Table 7.SM.6 of https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter07_SM.pdf
RADIATIVE_EFFICIENCIES: dict[str, pint.UnitRegistry.Quantity] = {
    "co2": Q(1.33e-5, "W / m^2 / ppb"),
    "ch4": Q(0.000388, "W / m^2 / ppb"),
    "n2o": Q(0.0032, "W / m^2 / ppb"),
    # Chlorofluorocarbons
    "cfc11": Q(0.291, "W / m^2 / ppb"),
    "cfc11eq": Q(0.291, "W / m^2 / ppb"),
    "cfc12": Q(0.358, "W / m^2 / ppb"),
    "cfc12eq": Q(0.358, "W / m^2 / ppb"),
    "cfc113": Q(0.301, "W / m^2 / ppb"),
    "cfc114": Q(0.314, "W / m^2 / ppb"),
    "cfc115": Q(0.246, "W / m^2 / ppb"),
    # Hydrofluorochlorocarbons
    "hcfc22": Q(0.214, "W / m^2 / ppb"),
    "hcfc141b": Q(0.161, "W / m^2 / ppb"),
    "hcfc142b": Q(0.193, "W / m^2 / ppb"),
    # Hydrofluorocarbons
    "hfc23": Q(0.191, "W / m^2 / ppb"),
    "hfc32": Q(0.111, "W / m^2 / ppb"),
    "hfc125": Q(0.234, "W / m^2 / ppb"),
    "hfc134a": Q(0.167, "W / m^2 / ppb"),
    "hfc134aeq": Q(0.167, "W / m^2 / ppb"),
    "hfc143a": Q(0.168, "W / m^2 / ppb"),
    "hfc152a": Q(0.102, "W / m^2 / ppb"),
    "hfc227ea": Q(0.273, "W / m^2 / ppb"),
    "hfc236fa": Q(0.251, "W / m^2 / ppb"),
    "hfc245fa": Q(0.245, "W / m^2 / ppb"),
    "hfc365mfc": Q(0.228, "W / m^2 / ppb"),
    "hfc4310mee": Q(0.357, "W / m^2 / ppb"),
    # Chlorocarbons and Hydrochlorocarbons
    "ch3ccl3": Q(0.065, "W / m^2 / ppb"),
    "ccl4": Q(0.166, "W / m^2 / ppb"),
    "ch3cl": Q(0.005, "W / m^2 / ppb"),
    "ch2cl2": Q(0.029, "W / m^2 / ppb"),
    "chcl3": Q(0.074, "W / m^2 / ppb"),
    # Bromocarbons, Hydrobromocarbons and Halons
    "ch3br": Q(0.004, "W / m^2 / ppb"),
    "halon1211": Q(0.300, "W / m^2 / ppb"),
    "halon1301": Q(0.299, "W / m^2 / ppb"),
    "halon2402": Q(0.312, "W / m^2 / ppb"),
    # Fully Fluorinated Species
    "nf3": Q(0.204, "W / m^2 / ppb"),
    "sf6": Q(0.567, "W / m^2 / ppb"),
    "so2f2": Q(0.211, "W / m^2 / ppb"),
    "cf4": Q(0.099, "W / m^2 / ppb"),
    "c2f6": Q(0.261, "W / m^2 / ppb"),
    "c3f8": Q(0.270, "W / m^2 / ppb"),
    "cc4f8": Q(0.314, "W / m^2 / ppb"),
    "c4f10": Q(0.369, "W / m^2 / ppb"),
    "c5f12": Q(0.408, "W / m^2 / ppb"),
    "c6f14": Q(0.449, "W / m^2 / ppb"),
    "c7f16": Q(0.503, "W / m^2 / ppb"),
    "c8f18": Q(0.558, "W / m^2 / ppb"),
}


def to_erf(indf: pd.DataFrame, out_unit="W / m^2") -> pd.DataFrame:
    """
    Convert to ERF

    Assumes linear radiative efficiencies,
    so is just an approximation.

    Parameters
    ----------
    indf
        Input [pd.DataFrame][pandas.DataFrame]

    out_unit
        Output unit

    Returns
    -------
    :
        Input converted to ERF
    """
    to_erf_conv_factor = pd.Series(
        index=indf.pix.unique(["gas", "unit"]),
        name="to_erf_conv_factor",
    )
    for gas, unit in to_erf_conv_factor.index:
        to_erf_conv_factor.loc[(gas, unit)] = (
            (RADIATIVE_EFFICIENCIES[gas] * Q(1, unit)).to(out_unit).m
        )

    erfs = indf.multiply(to_erf_conv_factor, axis="rows").pix.assign(unit=out_unit)

    return erfs
