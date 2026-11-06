"""Navigation line (NAVLNE, code 85). Geometry: Line."""

from .bearing import bearing_label, bearing_label_layer
from .prelude import *

LINE_COLOR = Color.CHGRD


class Navlne(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(LINE_COLOR)
        bearing_label(feature)

    def layers(self, b):
        return [
            b.line_layer_with_color(LINE_COLOR, width=1.0, style=LineStyle.custom_dash(10.0, 5.0)),
            bearing_label_layer(b),
        ]
