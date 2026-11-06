"""Radar transponder beacon (RTPBCN, code 103). Geometry: Point."""

from .prelude import *


class Rtpbcn(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("RTPBCN02")

    def layers(self, b):
        return [
            b.point_layer_from_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP),
            b.area_layer_with_point_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP),
        ]
