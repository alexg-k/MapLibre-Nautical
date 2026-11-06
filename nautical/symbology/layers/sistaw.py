"""Signal station, warning (SISTAW, code 124). Geometry: Point."""

from .prelude import *


class Sistaw(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("SISTAW03")

    def layers(self, b):
        return [b.point_layer_from_symbol(icon_offset=Offset.coord(0.0, -24.0))]
