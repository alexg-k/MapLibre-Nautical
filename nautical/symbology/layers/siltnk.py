"""Silo / tank (SILTNK, code 125). Geometry: Point, Area."""

from .prelude import *

AC = Color.CHBRN
LINE_COLORS = [Color.CHBLK, Color.LANDF]


class Siltnk(Layerable):
    def pre_tile_encode(self, feature, cx):
        convis = Convis.of(feature.props)
        conspicuous = convis == Convis.VISUAL_CONSPICUOUS
        category = Catsil.of(feature.props)
        if category == Catsil.SILO_IN_GENERAL:
            if conspicuous:
                feature.point_symbol("SILBUI11")
            else:
                feature.point_symbol("SILBUI01")
        elif category == Catsil.TANK_IN_GENERAL:
            if conspicuous:
                feature.point_symbol("TNKCON12")
            else:
                feature.point_symbol("TNKCON02")
        elif category == Catsil.GRAIN_ELEVATOR:
            if conspicuous:
                feature.point_symbol("TOWERS03")
            else:
                feature.point_symbol_n("TOWERS01", 2)
        elif category == Catsil.WATER_TOWER:
            if conspicuous:
                feature.point_symbol("TOWERS02")
            else:
                feature.point_symbol_n("TOWERS12", 2)
        else:
            feature.point_symbol("SILBUI01")
        if conspicuous:
            feature.line_color(Color.CHBLK)
        else:
            feature.line_color(Color.LANDF)
        feature.area_color(AC)

    def layers(self, b):
        return [
            b.area_layer_with_fill_color(AC),
            b.line_layer_with_colors(LINE_COLORS),
            b.point_layer_from_symbol(
                symbol=Symbol.prop(),
                anchor=Anchor.BOTTOM,
                icon_allow_overlap=True,
                icon_rotation_alignment=IconRotationAlignment.MAP,
            ),
            b.point_layer_from_symbol(
                symbol=Symbol.prop(2),
                anchor=Anchor.BOTTOM,
                icon_allow_overlap=True,
                icon_rotation_alignment=IconRotationAlignment.VIEWPORT,
            ),
        ]
