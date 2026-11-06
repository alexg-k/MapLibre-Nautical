"""Coastline (COALNE)."""

from .prelude import *


class Coalne(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(Color.CSTLN)

    def layers(self, b):
        return [b.line_layer_with_color(Color.CSTLN, width=1.0, style=LineStyle.custom_dash(5.0, 5.0))]
