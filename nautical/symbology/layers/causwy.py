"""Causeway (CAUSWY, code 26). Geometry: Line, Area."""

from .prelude import *

LINE_COLOR = Color.CSTLN

AREA_FILL_COLORS = [Color.CHBRN, Color.DEPIT]


class Causwy(Layerable):
    def pre_tile_encode(self, feature, cx):
        watlev = Watlev.of(feature.props)
        if watlev in (
            Watlev.PARTLY_SUBMERGED_AT_HIGH_WATER,
            Watlev.ALWAYS_UNDER_WATER_SUBMERGED,
            Watlev.AWASH,
            Watlev.SUBJECT_TO_INUNDATION_OR_FLOODING,
            Watlev.COVERS_AND_UNCOVERS,
        ):
            feature.area_color(Color.DEPIT)
        else:
            # ALWAYS_DRY, FLOATING, None
            feature.area_color(Color.CHBRN)

    def layers(self, b):
        return [
            b.area_layer_with_fill_colors(AREA_FILL_COLORS),
            b.line_layer_with_color(LINE_COLOR, style=LineStyle.DASH_LINE),
        ]
