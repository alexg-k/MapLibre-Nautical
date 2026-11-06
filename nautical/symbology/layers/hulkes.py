"""Hulk (HULKES, code 65). Geometry: Point, Area."""

from .prelude import *


class Hulkes(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("HULKES01")

    def layers(self, b):
        return [
            b.area_layer_with_fill_color(Color.CHBRN),
            b.line_layer_with_color(Color.CSTLN, width=2.0),
            b.point_layer_from_symbol(
                symbol=Symbol.of("HULKES01"),
                anchor=Anchor.CENTER,
                icon_allow_overlap=True,
                icon_rotation_alignment=IconRotationAlignment.MAP,
            ),
        ]
