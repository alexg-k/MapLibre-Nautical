"""Daymark (DAYMAR, code 39). Geometry: Point."""

from .prelude import *


class Daymar(Layerable):
    def pre_tile_encode(self, feature, cx):
        shape = Topshp.of(feature.props)
        if shape in (Topshp.SQUARE, Topshp.RECTANGLE_HORIZONTAL, Topshp.RECTANGLE_VERTICAL):
            symbol = "DAYSQR01"
        elif shape == Topshp.TRIANGLE_POINT_UP:
            symbol = "DAYTRI01"
        elif shape == Topshp.TRIANGLE_POINT_DOWN:
            symbol = "DAYTRI05"
        else:
            symbol = "DAYSQR01"
        feature.point_symbol(symbol)

    def layers(self, b):
        return [b.point_layer_from_symbol(icon_offset=Offset.coord(0.0, -18.0))]
