"""Beacon, lateral (BCNLAT, code 7). Geometry: Point.

Lateral beacons; ``Bcnsaw`` and ``Bcnspp`` reuse :func:`bcnshp`.
"""

from .prelude import *

_TALL = {Colour.RED: "BCNLAT21", Colour.GREEN: "BCNLAT22", Colour.BLACK: "BCNSAW21"}
_SHORT = {Colour.RED: "BCNLAT15", Colour.GREEN: "BCNLAT16", Colour.BLACK: "BCNSAW13"}


def bcnshp(feature):
    """The symbol by BCNSHP and the first colour, BCNDEF13 without a shape."""
    colour = Colour.first(feature.props)
    shape = Bcnshp.of(feature.props)
    if shape in (Bcnshp.STAKE_POLE_PERCH_POST, Bcnshp.WHITY):
        symbol = _TALL.get(colour, "BCNSPP21")  # yellow tall beacon
    elif shape in (Bcnshp.BEACON_TOWER, Bcnshp.LATTICE_BEACON, Bcnshp.PILE_BEACON):
        symbol = _SHORT.get(colour, "BCNSPP13")  # yellow short beacon
    elif shape == Bcnshp.CAIRN:
        symbol = "CAIRNS11"
    elif shape == Bcnshp.BUOYANT_BEACON:
        symbol = "BCNLAT21"
    else:
        symbol = "BCNDEF13"
    feature.point_symbol(symbol)


class Bcnlat(Layerable):
    def pre_tile_encode(self, feature, cx):
        bcnshp(feature)

    def layers(self, b):
        return [b.point_layer_from_symbol()]
