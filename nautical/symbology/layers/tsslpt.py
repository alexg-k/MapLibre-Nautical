"""Traffic separation scheme lane part (TSSLPT, code 148). Geometry: Area."""

from .prelude import *


class Tsslpt(Layerable):
    def pre_tile_encode(self, feature, cx):
        if float_value(feature.props, "ORIENT") is not None:
            feature.point_symbol("RCTLPT52")

    def layers(self, b):
        return [
            b.area_layer_with_point_symbol(
                icon_rotate=IconRot(prop="ORIENT"),
                icon_rotation_alignment=IconRotationAlignment.MAP,
                icon_allow_overlap=False,
            )
        ]
