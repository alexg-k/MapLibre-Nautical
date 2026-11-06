"""Deep water route centerline (DWRTCL, code 40). Geometry: Line."""

from .bearing import bearing_label, bearing_label_layer
from .prelude import *

LINE_COLOR = Color.CHBLK


class Dwrtcl(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(LINE_COLOR)
        bearing_label(feature)

    def layers(self, b):
        return [
            b.line_layer_with_color(LINE_COLOR),
            bearing_label_layer(b),
        ]
