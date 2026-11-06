"""Underwater rock / awash rock (UWTROC, code 152). Geometry: Point.

S-52 chooses the symbol by WATLEV (always under water: UWTROC04; covers and uncovers, awash or
flooding: UWTROC03); everything else gets the isolated danger symbol.
"""

from .prelude import *


class Uwtroc(Layerable):
    def pre_tile_encode(self, feature, cx):
        watlev = Watlev.of(feature.props)
        if watlev == Watlev.ALWAYS_UNDER_WATER_SUBMERGED:
            feature.point_symbol("UWTROC04")
        elif watlev in (
            Watlev.AWASH,
            Watlev.SUBJECT_TO_INUNDATION_OR_FLOODING,
            Watlev.PARTLY_SUBMERGED_AT_HIGH_WATER,
            Watlev.COVERS_AND_UNCOVERS,
        ):
            feature.point_symbol("UWTROC03")
        else:
            # ALWAYS_DRY, FLOATING, None
            feature.point_symbol("ISODGR01")

    def layers(self, b):
        return [b.point_layer_from_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP)]
