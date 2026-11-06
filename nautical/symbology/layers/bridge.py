"""Bridge (BRIDGE)."""

from .clearance_label import opening_bridge
from .prelude import *


class Bridge(Layerable):
    def pre_tile_encode(self, feature, cx):
        opening = any(
            c
            in (
                Catbrg.OPENING_BRIDGE,
                Catbrg.SWING_BRIDGE,
                Catbrg.LIFTING_BRIDGE,
                Catbrg.BASCULE_BRIDGE,
                Catbrg.DRAW_BRIDGE,
                Catbrg.TRANSPORTER_BRIDGE,
            )
            for c in Catbrg.of(feature.props)
        )
        if opening:
            feature.point_symbol("BRIDGE01")
            feature.line_pattern("BRIDGE01")
            opening_bridge(feature)

    def layers(self, b):
        return [
            b.line_layer_with_color(Color.CHGRD, width=4.0),
            b.point_layer_from_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP),
            b.line_layer_with_pattern(),
        ]
