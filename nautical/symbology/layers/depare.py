"""Depth area (DEPARE, code 42). Geometry: Line, Area."""

from .prelude import *

AREA_FILL_COLORS = [Color.DEPIT, Color.DEPVS, Color.DEPMS, Color.DEPMD, Color.DEPDW]


class Depare(Layerable):
    def layers(self, b):
        # DRVAL1 is the lower (shallower, sometimes negative) end of the range, DRVAL2 the deeper.
        return [
            b.area_layer_with_fill_colors(AREA_FILL_COLORS),
            b.line_layer_with_colors([Color.CHGRD], width=0.5),
        ]

    def pre_tile_encode(self, feature, cx):
        """The colour band by DRVAL1 against the configured thresholds (``<=`` at each), DEPIT
        for a drying area (DRVAL1 < 0 and DRVAL2 <= 0), CHBLK when either bound is missing."""
        config = cx.config
        ac = Color.CHBLK
        shallow_range = float_value(feature.props, "DRVAL1")
        deep_range = float_value(feature.props, "DRVAL2")
        if shallow_range is not None and deep_range is not None:
            if shallow_range < 0.0 and deep_range <= 0.0:
                ac = Color.DEPIT
            elif shallow_range <= config.shallow_depth:
                ac = Color.DEPVS
            elif shallow_range <= config.safety_depth:
                ac = Color.DEPMS
            elif shallow_range <= config.deep_depth:
                ac = Color.DEPMD
            else:
                ac = Color.DEPDW
        feature.area_color(ac)
        feature.line_color(Color.CHGRD)
