"""Traffic separation scheme roundabout (TSSRON, code 150). Geometry: Area."""

from .prelude import *

LINE_COLOR = Color.TRFCF


class Tssron(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [b.line_layer_with_color(LINE_COLOR, style=LineStyle.custom_dash(3.0, 2.0))]
