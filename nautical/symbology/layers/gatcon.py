"""Gate (GATCON, code 61). Geometry: Point, Line, Area."""

from .prelude import *

AREA_COLOR = Color.CHBRN
LINE_COLOR = Color.CSTLN


class Gatcon(Layerable):
    def pre_tile_encode(self, feature, cx):
        catgat = Catgat.of(feature.props)
        if catgat in (Catgat.FLOOD_BARRAGE_GATE, Catgat.CAISSON):
            feature.point_symbol("GATCON04")
            feature.line_pattern("GATCON04")
        elif catgat == Catgat.LOCK_GATE:
            feature.point_symbol("GATCON03")
            feature.line_pattern("GATCON03")
        feature.area_color(AREA_COLOR)
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [
            b.point_layer_from_symbol(),
            b.area_layer_with_fill_color(AREA_COLOR),
            b.line_layer_with_color(LINE_COLOR, width=2.0),
            b.line_layer_with_pattern(
                include_polygon_lines=False,
                symbol_placement=Placement.LINE_CENTER,
                icon_rotation_alignment=IconRotationAlignment.VIEWPORT,
                icon_allow_overlap=True,
            ),
        ]
