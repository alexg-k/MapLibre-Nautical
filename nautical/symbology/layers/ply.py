"""The ``PLY`` source layer (``factory.extra_layers``): a CURSR outline at zooms 0-9."""

from .prelude import *


class Ply(Layerable):
    def layers(self, b):
        return [
            b.layer(
                f"{b.key}_line",
                LayerType.LINE,
                filter=[filters.ANY, filters.eq_type_line_string()],
                paint=paint(line_color=b.color(Color.CURSR), line_width=2.0),
                minzoom=0,
                maxzoom=10,
            )
        ]
