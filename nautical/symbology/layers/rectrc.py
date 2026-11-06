"""Recommended track (RECTRC, code 109). Geometry: Line, Area."""

from .bearing import bearing_label, bearing_label_layer
from .prelude import *


class Rectrc(Layerable):
    def pre_tile_encode(self, feature, cx):
        bearing_label(feature)
        trafic = Trafic.of(feature.props)
        if Cattrk.of(feature.props) == Cattrk.BASED_ON_A_SYSTEM_OF_MARKS:
            if trafic in (Trafic.INBOUND, Trafic.OUTBOUND, Trafic.ONE_WAY):
                feature.line_pattern("RECTRC58")
            elif trafic == Trafic.TWO_WAY:
                feature.line_pattern("RECTRC56")
            else:
                feature.line_pattern("RECDEF51")
        else:
            # NOT_BASED_ON_A_SYSTEM_OF_MARKS, None
            if trafic in (Trafic.INBOUND, Trafic.OUTBOUND, Trafic.ONE_WAY):
                feature.line_pattern("RECTRC57")
            elif trafic == Trafic.TWO_WAY:
                feature.line_pattern("RECTRC55")
            else:
                feature.line_pattern("RECDEF51")

    def layers(self, b):
        return [
            # Map rotation alignment lines the icon's x-axis up with the line.
            b.line_layer_with_spaced_pattern(False, icon_rotate=90.0, spacing=15.0),
            bearing_label_layer(b),
        ]
