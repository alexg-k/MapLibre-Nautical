"""Oil barrier (OILBAR, code 89). Geometry: Line."""

from .prelude import *

LINE_COLOR = Color.CHBLK


class Oilbar(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [b.line_layer_with_color(LINE_COLOR, style=LineStyle.DASH_LINE)]
