"""Obstruction (OBSTRN, code 86). Geometry: Point, Line, Area.

Two layerables read the OBSTRN source layer: :class:`ObstrnArea` draws the area fill and outline
with the land layers, :class:`Obstrn` the symbol and depth text with the other obstructions.
:class:`Obstrn` reuses the ``soundg`` text layers for its depth text.
"""

from . import soundg
from .prelude import *


class ObstrnArea(Layerable):
    source_layer = "OBSTRN"

    def layers(self, b):
        return [
            b.area_layer_with_fill_colors([d.color() for d in DepthColor]),
            b.area_layer_with_fill_pattern(None),
            b.line_layer_with_color(Color.CHGRD, style=LineStyle.DASH_LINE),
        ]


class Obstrn(Layerable):
    def layers(self, b):
        layers = [
            b.point_layer_from_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP),
            b.area_layer_with_point_symbol(icon_rotation_alignment=IconRotationAlignment.MAP),
        ]
        layers.extend(soundg.text_layers(b))
        return layers

    def pre_tile_encode(self, feature, cx):
        state = ObstrnState(feature)

        sy_set = False
        show_depth = state.usable_depth_value
        fill_depth_color = True

        category = state.category
        if category in (Catobs.SNAG_STUMP, Catobs.WELLHEAD, Catobs.DIFFUSER, Catobs.CRIB):
            if not state.usable_depth_value:
                feature.point_symbol("ISODGR01")
                sy_set = True
                show_depth = False
        elif category == Catobs.FISH_HAVEN:
            feature.point_symbol("FSHHAV01")
            sy_set = True
            show_depth = False
        elif category in (Catobs.FOUL_AREA, Catobs.FOUL_GROUND):
            feature.area_pattern("FOULAR01P")
        elif category == Catobs.GROUND_TACKLE:
            feature.point_symbol("ACHARE02")
            sy_set = True
            show_depth = False
        elif category in (Catobs.ICE_BOOM, Catobs.BOOM):
            feature.point_symbol("FLTHAZ02")

        check_accuracy = True
        if not sy_set:
            watlev = state.water_level_effect
            if watlev == Watlev.COVERS_AND_UNCOVERS:
                check_accuracy = False
                feature.exclude_area_point_symbol()
                feature.point_symbol("OBSTRN03")
            elif watlev == Watlev.ALWAYS_DRY:
                check_accuracy = False
                feature.exclude_area_point_symbol()
                feature.point_symbol("OBSTRN11")
            elif watlev == Watlev.ALWAYS_UNDER_WATER_SUBMERGED:
                feature.exclude_area_point_symbol()
                band = state.depth_color(cx)
                if band in (DepthColor.DEEP_WATER, DepthColor.MEDIUM_DEPTH):
                    shown, hidden = "DANGER02", "OBSTRN02"
                elif band in (DepthColor.SAFETY_DEPTH, DepthColor.VERY_SHALLOW):
                    shown, hidden = "DANGER01", "OBSTRN01"
                else:
                    shown, hidden = "DANGER03", "OBSTRN03"
                feature.point_symbol(shown if show_depth else hidden)
            elif watlev == Watlev.FLOATING:
                show_depth = False
                fill_depth_color = False
                feature.point_symbol("FLTHAZ02")
            else:
                # PARTLY_SUBMERGED_AT_HIGH_WATER, AWASH, SUBJECT_TO_INUNDATION_OR_FLOODING, None
                check_accuracy = False
                feature.point_symbol("ISODGR01")

        if check_accuracy and any(
            q in (Quasou.DOUBTFUL_SOUNDING, Quasou.UNRELIABLE_SOUNDING) for q in state.quality_of_sounding
        ):
            show_depth = False
            feature.point_symbol("LOWACC01")

        if fill_depth_color:
            feature.area_color(state.depth_color(cx).color())
        if show_depth and state.meters is not None:
            add_sounding_conversions(feature.props, float(state.meters))


class ObstrnState:
    """The attributes an obstruction's symbology reads."""

    def __init__(self, feature):
        self.quality_of_sounding = Quasou.of(feature.props)
        first = self.quality_of_sounding[0] if self.quality_of_sounding else None
        self.usable_depth_value = first in (
            Quasou.DEPTH_KNOWN,
            Quasou.NO_BOTTOM_FOUND_AT_VALUE_SHOWN,
            Quasou.LEAST_DEPTH_KNOWN,
            Quasou.LEAST_DEPTH_UNKNOWN_SAFE_CLEARANCE_AT_VALUE_SHOWN,
            Quasou.MAINTAINED_DEPTH,
        )
        self.meters = float_value(feature.props, "VALSOU")
        self.category = Catobs.of(feature.props)
        self.water_level_effect = Watlev.of(feature.props)

    def depth_color(self, cx):
        """COVERS_UNCOVERS unless always submerged, then by a usable VALSOU against the
        thresholds (VERY_SHALLOW without one)."""
        config = cx.config
        if self.water_level_effect == Watlev.ALWAYS_UNDER_WATER_SUBMERGED:
            m = self.meters
            if m is None or not self.usable_depth_value:
                return DepthColor.VERY_SHALLOW
            if m <= config.shallow_depth:
                return DepthColor.VERY_SHALLOW
            if m <= config.safety_depth:
                return DepthColor.SAFETY_DEPTH
            if m <= config.deep_depth:
                return DepthColor.MEDIUM_DEPTH
            return DepthColor.DEEP_WATER
        return DepthColor.COVERS_UNCOVERS
