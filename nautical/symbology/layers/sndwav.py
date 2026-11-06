"""Sand waves (SNDWAV, code 118). Geometry: Point, Line, Area."""

from .prelude import *


class Sndwav(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(Color.CHGRD)
        feature.area_pattern("SNDWAV01P")
        feature.point_symbol("SNDWAV02")

    def layers(self, b):
        return [
            b.point_layer_from_symbol(),
            b.line_layer_with_color(Color.CHGRD, style=LineStyle.DASH_LINE),
            b.area_layer_with_point_symbol(),
        ]
