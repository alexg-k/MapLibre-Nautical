"""Sea area / named water area (SEAARE, code 119). Geometry: Point, Area."""

from .prelude import *


class Seaare(Layerable):
    def layers(self, b):
        return [
            b.area_layer_with_text(
                Label(prop="OBJNAM"),
                text_color=Color.SNDG2,
                halo_color=Color.DEPDW,
                text_justify=TextJustify.LEFT,
                text_offset=Offset.coord(4.0, 2.0),
                text_optional=True,
            )
        ]
