"""Recommended Traffic Lane Part (RCTLPT, code 110). Geometry: Point, Area."""

from .prelude import *


class Rctlpt(Layerable):
    def pre_tile_encode(self, feature, cx):
        if float_value(feature.props, "ORIENT") is not None:
            feature.point_symbol("RCTLPT52")
        else:
            feature.point_symbol("RTLDEF51")

    def layers(self, b):
        return [
            b.point_layer_from_symbol(
                icon_rotate=IconRot(prop="ORIENT"),
                icon_rotation_alignment=IconRotationAlignment.MAP,
                icon_allow_overlap=False,
            ),
            b.area_layer_with_point_symbol(
                icon_rotate=IconRot(prop="ORIENT"),
                icon_rotation_alignment=IconRotationAlignment.MAP,
                icon_allow_overlap=False,
            ),
        ]
