"""Fishing facility (FSHFAC, code 55). Geometry: Point, Line, Area."""

from .prelude import *


class Fshfac(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(Color.CHGRD)
        category = Catfif.of(feature.props)
        if category == Catfif.FISHING_STAKE:
            feature.point_symbol("FSHFAC03")
            feature.area_pattern("FSHFAC03")
        elif category in (Catfif.FISH_TRAP, Catfif.FISH_WEIR, Catfif.TUNNY_NET):
            feature.point_symbol("FSHFAC02")
            feature.area_pattern("FSHFAC04P")
        else:
            feature.point_symbol("FSHFAC02")
            feature.area_pattern("FSHHAV02P")

    def layers(self, b):
        return [
            b.line_layer_with_color(Color.CHGRD, style=LineStyle.DASH_LINE, width=1.0),
            b.point_layer_from_symbol(),
        ]
