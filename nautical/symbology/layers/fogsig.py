"""Fog signal (FOGSIG, code 58). Geometry: Point."""

from .prelude import *


class Fogsig(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("FOGSIG01")

    def layers(self, b):
        return [b.point_layer_from_symbol(icon_offset=Offset.coord(-10.0, 10.0), icon_allow_overlap=True)]
