"""Fairway (FAIRWY, code 51). Geometry: Area."""

from .prelude import *

LINE_COLOR = Color.CHBLK


class Fairwy(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [b.line_layer_with_color(LINE_COLOR, width=0.5, style=LineStyle.custom_dash(10.0, 5.0))]
