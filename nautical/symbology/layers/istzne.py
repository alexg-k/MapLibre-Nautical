"""Inshore traffic zone (ISTZNE, code 68). Geometry: Area."""

from .prelude import *

LINE_COLOR = Color.TRFCD


class Istzne(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [b.line_layer_with_color(LINE_COLOR, style=LineStyle.DASH_LINE, width=1.0)]
