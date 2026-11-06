"""Pipeline area (PIPARE, code 92). Geometry: Point, Area."""

from .prelude import *

LINE_COLOR = Color.CHMGD
SYMBOL = "CHINFO07"


class Pipare(Layerable):
    def pre_tile_encode(self, feature, cx):
        catpip = Catpip.of(feature.props)
        if any(c in (Catpip.OUTFALL_PIPE, Catpip.INTAKE_PIPE) for c in catpip):
            color = Color.CHGRD
        else:
            prodct = Prodct.of(feature.props)
            if prodct and prodct[0] == Prodct.WATER:
                color = Color.CHGRD
            else:
                color = Color.CHMGD
        feature.line_color(color)
        feature.point_symbol(SYMBOL)

    def layers(self, b):
        return [
            b.line_layer_with_color(LINE_COLOR, style=LineStyle.DASH_LINE),
            b.point_layer_from_symbol(
                symbol=Symbol.of(SYMBOL),
                anchor=Anchor.CENTER,
                icon_rotation_alignment=IconRotationAlignment.MAP,
            ),
        ]
