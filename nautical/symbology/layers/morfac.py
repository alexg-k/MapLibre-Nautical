"""Mooring/warping facility (MORFAC, code 84). Geometry: Point, Line, Area."""

from .prelude import *


class Morfac(Layerable):
    def pre_tile_encode(self, feature, cx):
        category = Catmor.of(feature.props)
        if category == Catmor.DOLPHIN:
            feature.point_symbol("MORFAC03")
        elif category == Catmor.DEVIATION_DOLPHIN:
            feature.point_symbol("MORFAC04")
        elif category == Catmor.BOLLARD:
            feature.point_symbol("PILPNT02")
        elif category == Catmor.POST_OR_PILE:
            feature.point_symbol("PILPNT02")
        elif category == Catmor.MOORING_BUOY:
            feature.point_symbol_n("BOYMOR11", 2)
        else:
            # TIE_UP_WALL, CHAIN_WIRE_CABLE, None
            feature.point_symbol("MORFAC03")

    def layers(self, b):
        return [
            b.area_layer_with_fill_color(Color.CHBRN),
            b.line_layer_with_color(Color.CHBRN, width=1.0),
            b.line_layer_with_color(
                Color.CSTLN,
                width=2.0,
                filter=[filters.ALL, filters.eq_type_line_string(), Catmor.TIE_UP_WALL.filter_eq()],
            ),
            b.line_layer_with_color(
                Color.CHMGF,
                width=1.0,
                style=LineStyle.custom_dash(5.0, 5.0),
                filter=[filters.ALL, filters.eq_type_line_string(), Catmor.CHAIN_WIRE_CABLE.filter_eq()],
            ),
            b.line_layer_with_color(
                Color.CSTLN,
                width=2.0,
                filter=[
                    filters.ALL,
                    filters.eq_type_line_string(),
                    Catmor.CHAIN_WIRE_CABLE.filter_not_eq(),
                    Catmor.TIE_UP_WALL.filter_not_eq(),
                ],
            ),
            b.point_layer_from_symbol(symbol=Symbol.prop(), icon_rotation_alignment=IconRotationAlignment.MAP),
            b.point_layer_from_symbol(symbol=Symbol.prop(2), icon_rotation_alignment=IconRotationAlignment.VIEWPORT),
        ]
