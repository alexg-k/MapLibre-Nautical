"""Berth (BERTHS, code 10). Geometry: Point, Line, Area."""

from .prelude import *


class Berths(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("BRTHNO01")
        feature.line_color(Color.CHMGD)

    def layers(self, b):
        label = Label(prop="OBJNAM")
        return [
            b.area_layer_with_point_symbol(),
            b.point_layer_from_symbol(),
            b.line_layer_with_color(Color.CHMGD, style=LineStyle.DASH_LINE),
            b.area_layer_with_text(label, text_color=Color.CHBLK, halo_color=Color.CHWHT),
            b.point_layer_with_label(label, label_color=Color.CHBLK, highlight_color=Color.CHWHT),
        ]
