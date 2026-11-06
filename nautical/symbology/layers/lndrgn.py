"""Land region (LNDRGN, code 73). Geometry: Point, Area."""

from .prelude import *


class Lndrgn(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("POSGEN04")
        if any(c in (Catlnd.SWAMP, Catlnd.MARSH) for c in Catlnd.of(feature.props)):
            feature.area_pattern("MARSHES1P")

    def layers(self, b):
        return [
            b.point_layer_from_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP),
            b.area_layer_with_fill_pattern(None),
            b.area_layer_with_text(Label(prop="OBJNAM"), text_color=Color.CHBLK, halo_color=Color.CHWHT),
        ]
