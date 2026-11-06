"""Sounding depths split into the metre, foot and fathom parts the depth labels show."""

from dataclasses import dataclass

from .number import sign


@dataclass(frozen=True)
class DisplayDepths:
    meters: float
    meters_whole: int
    meters_tenths: int
    feet: int
    fathoms: int
    fathoms_feet: int


def display_depths(meters):
    """Splits a sounding in metres into its display parts.

    Every part is computed on the magnitude and then given the sounding's sign, so a drying
    height (negative, S-57 convention) carries the same digits as the equivalent depth with every
    part negative.
    """
    magnitude = abs(meters)
    sgn = int(sign(meters))

    feet = magnitude * 3.28084
    feet_whole = int(feet)
    if feet - feet_whole >= 0.9:
        feet_whole += 1
    fathoms = magnitude * 0.546807
    fathoms_whole = int(fathoms)
    fathoms_feet = int((fathoms - fathoms_whole) * 6.0)
    # S-57 encodes depths to one decimal, so split on the decimal tenths rather than the binary
    # double: 2.3 is 2.29999... and truncating (2.3 - 2) * 10 would read 2.2.
    tenths_total = int((magnitude * 10.0 + 1e-6) // 1)
    return DisplayDepths(
        meters=meters,
        meters_whole=sgn * (tenths_total // 10),
        meters_tenths=sgn * (tenths_total % 10),
        feet=sgn * feet_whole,
        fathoms=sgn * fathoms_whole,
        fathoms_feet=sgn * fathoms_feet,
    )


def add_sounding_conversions(props, meters):
    """Writes ``METERS``, ``METERS_W``, ``METERS_T``, ``FEET``, ``FATHOMS``, ``FATHOMS_FT``."""
    d = display_depths(meters)
    props["METERS"] = meters
    props["METERS_W"] = d.meters_whole
    props["METERS_T"] = d.meters_tenths
    props["FEET"] = d.feet
    props["FATHOMS"] = d.fathoms
    props["FATHOMS_FT"] = d.fathoms_feet
