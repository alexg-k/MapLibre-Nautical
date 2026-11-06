"""Inland ENC object NOTMRK: registered in ``inland_layers``, but draws nothing yet."""

from .prelude import *


class Notmrk(Layerable):
    def layers(self, b):
        return []
