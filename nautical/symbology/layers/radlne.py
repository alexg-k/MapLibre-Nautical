"""Radar line (RADLNE, code 99). Geometry: Line."""

from .bearing import bearing_label, bearing_label_layer
from .prelude import *


class Radlne(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(Color.TRFCD)
        bearing_label(feature)

    def layers(self, b):
        return [
            b.line_layer_with_color(Color.TRFCD, style=LineStyle.DASH_LINE),
            bearing_label_layer(b),
        ]
