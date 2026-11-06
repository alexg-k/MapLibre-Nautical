"""Ferry route (FERYRT, code 53). Geometry: Line, Area."""

from .prelude import *

LINE_COLOR = Color.CHBLK


class Feryrt(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(LINE_COLOR)
        feature.line_pattern("FRYARE51")

    def layers(self, b):
        return [
            b.line_layer_with_color(LINE_COLOR, style=LineStyle.custom_dash(6.0, 2.0)),
            b.line_layer_with_pattern(symbol="FRYARE51"),
        ]
