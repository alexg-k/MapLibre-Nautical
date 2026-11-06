"""Conveyor (CONVYR, code 34). Geometry: Line, Area."""

from .prelude import *


class Convyr(Layerable):
    def layers(self, b):
        return [
            b.line_layer_with_color(Color.CHGRD, width=0.5),
            b.line_layer_with_pattern(),
        ]

    def pre_tile_encode(self, feature, cx):
        if Conrad.of(feature.props) in (Conrad.RADAR_CONSPICUOUS, Conrad.RADAR_CONSPICUOUS_HAS_RADAR_REFLECTOR):
            feature.line_pattern("RACNSP01")
