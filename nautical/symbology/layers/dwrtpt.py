"""Deep water route part (DWRTPT, code 41). Geometry: Area."""

from .prelude import *


class Dwrtpt(Layerable):
    def pre_tile_encode(self, feature, cx):
        if float_value(feature.props, "ORIENT") is not None:
            trafic = Trafic.of(feature.props)
            if trafic in (Trafic.INBOUND, Trafic.OUTBOUND, Trafic.ONE_WAY):
                feature.point_symbol("TSSLPT51")
            elif trafic == Trafic.TWO_WAY:
                feature.point_symbol("DWRUTE51")

    def layers(self, b):
        return [
            b.area_layer_with_point_symbol(
                icon_rotate=IconRot(prop="ORIENT"),
                icon_rotation_alignment=IconRotationAlignment.MAP,
                icon_allow_overlap=False,
            )
        ]
