"""Recommended track center line (RCRTCL, code 107). Geometry: Line."""

from .bearing import bearing_label, bearing_label_layer
from .prelude import *


class Rcrtcl(Layerable):
    def pre_tile_encode(self, feature, cx):
        bearing_label(feature)

    def layers(self, b):
        return [
            b.line_layer_with_color(Color.PLRTE),
            bearing_label_layer(b),
        ]
