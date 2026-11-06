"""Cable area (CBLARE, code 20). Geometry: Area."""

from .prelude import *

LINE_COLOR = Color.CHMGD


class Cblare(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("CBLARE51")
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [
            b.line_layer_with_color(LINE_COLOR, style=LineStyle.custom_dash(3.0, 2.0)),
            # give room for resare
            b.area_layer_with_single_symbol(
                icon_offset=[30.0, 30.0],
                anchor=Anchor.CENTER,
                icon_rotation_alignment=IconRotationAlignment.MAP,
            ),
        ]
