"""Traffic separation line (TSELNE, code 145). Geometry: Line."""

from .prelude import *

LINE_COLOR = Color.TRFCF


class Tselne(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [b.line_layer_with_color(LINE_COLOR, width=6.0)]
