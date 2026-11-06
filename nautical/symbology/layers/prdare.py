"""Production / storage area (PRDARE, code 97). Geometry: Point, Area."""

from .prelude import *

_SYMBOLS = {
    Catpra.QUARRY: "QUARRY01",
    Catpra.MINE: "PRDINS02",
    Catpra.STOCKPILE: "PRDINS02",
    Catpra.POWER_STATION_AREA: "PRDINS02",
    Catpra.REFINERY_AREA: "RFNERY11",
    Catpra.TIMBER_YARD: "TMBYRD01",
    Catpra.FACTORY_AREA: "PRDINS02",
    Catpra.TANK_FARM: "TNKFRM11",
    Catpra.WIND_FARM: "WNDFRM61",
}


class Prdare(Layerable):
    def pre_tile_encode(self, feature, cx):
        if Convis.of(feature.props) == Convis.VISUAL_CONSPICUOUS:
            line_color = Color.CHBLK
        else:
            # NOT_VISUAL_CONSPICUOUS, None
            line_color = Color.LANDF

        feature.line_color(line_color)

        symbol = _SYMBOLS.get(Catpra.of(feature.props))

        if symbol is not None:
            feature.point_symbol(symbol)
            feature.line_pattern(symbol)

    def layers(self, b):
        return [
            b.point_layer_from_symbol(),
            b.line_layer_with_colors([Color.LANDF, Color.CHBLK], style=LineStyle.DASH_LINE),
            b.line_layer_with_pattern(),
        ]
