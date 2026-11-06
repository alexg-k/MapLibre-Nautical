"""Radar range (RADRNG, code 100). Geometry: Area."""

from .prelude import *


class Radrng(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(Color.TRFCF)

    def layers(self, b):
        return [b.line_layer_with_color(Color.TRFCF, width=1.0, style=LineStyle.DASH_LINE)]
