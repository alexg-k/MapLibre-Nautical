"""Inland ENC object EXCNST: registered in ``inland_layers``, but draws nothing yet."""

from .prelude import *


class Excnst(Layerable):
    def layers(self, b):
        return []
