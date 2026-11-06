"""Two-way route part (TWRTPT, code 152). Geometry: Area."""

from .prelude import *

LINE_COLOR = Color.TRFCF


class Twrtpt(Layerable):
    def pre_tile_encode(self, feature, cx):
        trafic = Trafic.of(feature.props)
        if trafic in (Trafic.INBOUND, Trafic.OUTBOUND, Trafic.ONE_WAY):
            feature.point_symbol("TWRTPT53")
        elif trafic == Trafic.TWO_WAY:
            feature.point_symbol("TWRTPT52")
        else:
            feature.point_symbol("TWRDEF51")
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [
            b.line_layer_with_color(LINE_COLOR, width=2.0, style=LineStyle.custom_dash(3.0, 2.0)),
            b.area_layer_with_point_symbol(
                icon_rotate=IconRot(prop="ORIENT"),
                icon_rotation_alignment=IconRotationAlignment.MAP,
                icon_allow_overlap=False,
            ),
        ]
