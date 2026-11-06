"""Dredged area (DRGARE, code 46). Geometry: Area."""

from .prelude import *

AREA_FILL_COLORS = [Color.DEPIT, Color.DEPVS, Color.DEPMS, Color.DEPMD, Color.DEPDW]


class Drgare(Layerable):
    def pre_tile_encode(self, feature, cx):
        config = cx.config
        ac = Color.DEPVS
        drval1 = float_value(feature.props, "DRVAL1")
        if drval1 is not None:
            if drval1 <= 0.0:
                ac = Color.DEPIT
            elif drval1 <= config.shallow_depth:
                ac = Color.DEPVS
            elif drval1 <= config.safety_depth:
                ac = Color.DEPMS
            elif drval1 <= config.deep_depth:
                ac = Color.DEPMD
            else:
                ac = Color.DEPDW
        feature.area_color(ac)
        feature.area_pattern("DRGARE01P")
        feature.line_color(Color.CHGRD)

    def layers(self, b):
        return [
            b.area_layer_with_fill_colors(AREA_FILL_COLORS),
            b.area_layer_with_fill_pattern(None),
            b.line_layer_with_colors([Color.CHGRD], width=0.5, style=LineStyle.DASH_LINE),
        ]
