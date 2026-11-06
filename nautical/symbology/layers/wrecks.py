"""Wreck (WRECKS, code 159). Geometry: Point, Area."""

from .prelude import *


class Wrecks(Layerable):
    def pre_tile_encode(self, feature, cx):
        """WRECKS01 (hull showing above water) visible above the surface; WRECKS05 (fishbone with
        dotted circle) dangerous, submerged, depth unknown; WRECKS04 (fishbone) non-dangerous;
        DANGER01 (hazard symbol with depth text) depth known, at or under the safety depth;
        ISODGR01 (magenta "screw head") hazard in otherwise safe water."""
        category = Catwrk.of(feature.props)
        if category == Catwrk.DANGEROUS_WRECK:
            feature.point_symbol("WRECKS05")
        elif category in (
            Catwrk.WRECK_SHOWING_MAST_MASTS,
            Catwrk.WRECK_SHOWING_ANY_PORTION_OF_HULL_OR_SUPERSTRUCTURE,
        ):
            feature.point_symbol("WRECKS01")
        else:
            # DISTRIBUTED_REMAINS_OF_WRECK, NON_DANGEROUS_WRECK, None
            # Despite the name, True means *deeper* than the safety depth.
            valsou = float_value(feature.props, "VALSOU")
            under_safety = None if valsou is None else valsou > cx.config.safety_depth
            if (
                Watlev.of(feature.props) == Watlev.ALWAYS_UNDER_WATER_SUBMERGED and under_safety is None
            ) or under_safety is True:
                feature.point_symbol("WRECKS04")
            elif under_safety is False:
                feature.point_symbol("DANGER01")
            else:
                feature.point_symbol("ISODGR01")

    def layers(self, b):
        return [b.point_layer_from_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP)]
