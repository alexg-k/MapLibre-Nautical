"""Restricted area (RESARE, code 112). Geometry: Area."""

from .prelude import *

LINE_COLOR = Color.CHMGD


class Resare(Layerable):
    def pre_tile_encode(self, feature, cx):
        restrictions = Restrn.of(feature.props)
        if any(it in (Restrn.ENTRY_RESTRICTED, Restrn.ENTRY_PROHIBITED) for it in restrictions):
            feature.point_symbol("ENTRES51")
        if any(it in (Restrn.ANCHORING_PROHIBITED, Restrn.ANCHORING_RESTRICTED) for it in restrictions):
            feature.point_symbol("ACHRES51")
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [
            b.line_layer_with_color(LINE_COLOR, style=LineStyle.custom_dash(3.0, 2.0)),
            b.point_layer_from_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP),
        ]
