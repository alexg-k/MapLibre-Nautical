"""Control point (CTRPNT, code 33). Geometry: Point."""

from .prelude import *


class Ctrpnt(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("POSGEN04")

    def layers(self, b):
        return [
            b.point_layer_from_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP),
            b.point_layer_with_label(
                Label(prop="OBJNAM"),
                text_anchor=Anchor.BOTTOM_LEFT,
                text_offset=Offset.coord(1.0, 0.0),
                highlight_color=Color.LANDA,
            ),
        ]
