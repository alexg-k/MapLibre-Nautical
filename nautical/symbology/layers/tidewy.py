"""Tideway (TIDEWY, code 147). Geometry: Line, Area.

S-52 lookup (area): ``LS(DASH,1,CHGRF);TX(OBJNAM,1,2,3,'15110',0,0,CHBLK,25)`` - a dashed outline
and a centred name, no fill. The presentation library has no line lookup, so a line gets the
same treatment.
"""

from .prelude import *


class Tidewy(Layerable):
    def layers(self, b):
        return [
            b.line_layer_with_color(Color.CHGRF, width=1.0, style=LineStyle.DASH_LINE),
            b.text_layer(["get", "OBJNAM"], filter=["has", "OBJNAM"]),
        ]
