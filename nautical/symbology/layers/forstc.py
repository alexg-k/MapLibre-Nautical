"""Fortified structure (FORSTC, code 59). Geometry: Point, Line, Area."""

from .prelude import *

LINE_COLORS = [Color.LANDF, Color.CHBLK]


class Forstc(Layerable):
    def pre_tile_encode(self, feature, cx):
        if Convis.of(feature.props) == Convis.VISUAL_CONSPICUOUS:
            feature.point_symbol("FORSTC11")
            feature.line_color(Color.CHBLK)
            feature.area_color(Color.CHBRN)
        else:
            # NOT_VISUAL_CONSPICUOUS, None
            feature.point_symbol("FORSTC11")
            feature.line_color(Color.LANDF)
            feature.area_color(Color.CHBRN)

    def layers(self, b):
        return [
            b.point_layer_from_symbol(),
            b.area_layer_with_fill_color(Color.CHBRN),
            b.line_layer_with_colors(LINE_COLORS),
        ]
