"""Buoy, lateral (BOYLAT, code 17). Geometry: Point.

``Boyspp`` reuses :func:`boyshp`.
"""

from .prelude import *


def half_triangle(feature):
    first = Colour.first(feature.props)
    feature.point_symbol({Colour.RED: "BOYLAT14", Colour.GREEN: "BOYLAT13"}.get(first, "BOYSPP15"))


def rhomboid(feature):
    first = Colour.first(feature.props)
    feature.point_symbol({Colour.RED: "BOYLAT24", Colour.GREEN: "BOYLAT23"}.get(first, "BOYSPP25"))


def circle(feature):
    first = Colour.first(feature.props)
    feature.point_symbol("BOYSAW12" if first == Colour.RED else "BOYSPP11")


def stake(feature):
    """Pillar and spar buoys get the tall beacon symbols."""
    first = Colour.first(feature.props)
    feature.point_symbol(
        {Colour.RED: "BCNLAT21", Colour.GREEN: "BCNLAT22", Colour.BLACK: "BCNSAW21"}.get(first, "BCNSPP21")
    )


def boyshp(feature):
    """The symbol by BOYSHP, BOYDEF03 without one."""
    shape = Boyshp.of(feature.props)
    if shape == Boyshp.CONICAL:
        half_triangle(feature)
    elif shape == Boyshp.CAN:
        rhomboid(feature)
    elif shape == Boyshp.SPHERICAL:
        circle(feature)
    elif shape in (Boyshp.PILLAR, Boyshp.SPAR):
        stake(feature)
    elif shape in (Boyshp.BARREL, Boyshp.SUPERBUOY, Boyshp.ICEBUOY):
        circle(feature)
    else:
        feature.point_symbol("BOYDEF03")


class Boylat(Layerable):
    def pre_tile_encode(self, feature, cx):
        category = Catlam.of(feature.props)
        if category == Catlam.PORT_HAND_LATERAL_MARK:
            rhomboid(feature)
        elif category == Catlam.STARBOARD_HAND_LATERAL_MARK:
            half_triangle(feature)
        elif category == Catlam.PREFERRED_CHANNEL_TO_STARBOARD_LATERAL_MARK:
            rhomboid(feature)
        elif category == Catlam.PREFERRED_CHANNEL_TO_PORT_LATERAL_MARK:
            half_triangle(feature)
        else:
            boyshp(feature)

    def layers(self, b):
        return [b.point_layer_from_symbol()]
