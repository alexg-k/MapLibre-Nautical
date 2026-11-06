"""The style's background, NODTA."""

from .prelude import *


class Background(Layerable):
    def layers(self, b):
        layer = b.layer("background", LayerType.BACKGROUND, paint=paint(background_color=b.color(Color.NODTA), background_opacity=1))
        del layer["source"], layer["source-layer"]
        return [layer]
