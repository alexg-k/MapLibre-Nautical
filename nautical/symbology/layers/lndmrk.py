"""Landmark (LNDMRK, code 74). Geometry: Point, Line, Area."""

from .prelude import *

LINE_COLORS = [Color.LANDF, Color.CHBLK]


class Lndmrk(Layerable):
    def pre_tile_encode(self, feature, cx):
        functn = Functn.of(feature.props)
        viz = False
        if Convis.of(feature.props) == Convis.VISUAL_CONSPICUOUS:
            viz = True
            feature.area_color(Color.CHBRN)
            feature.line_color(Color.CHBLK)
        else:
            # NOT_VISUAL_CONSPICUOUS, None
            feature.area_color(Color.CHBRN)
            feature.line_color(Color.LANDF)

        def pick(conspicuous, other):
            return conspicuous if viz else other

        if any(f in (Functn.CHURCH, Functn.CHAPEL) for f in functn):
            feature.point_symbol(pick("BUIREL13", "BUIREL01"))
            return

        if any(f in (Functn.MOSQUE, Functn.MARABOUT) for f in functn):
            feature.point_symbol(pick("BUIREL15", "BUIREL05"))
            return

        categories = Catlmk.of(feature.props)
        category = categories[0] if categories else None
        if category == Catlmk.CAIRN:
            symbol = pick("CAIRNS11", "CAIRNS01")
        elif category == Catlmk.CHIMNEY:
            symbol = pick("CHIMNY11", "CHIMNY01")
        elif category == Catlmk.DISH_AERIAL:
            symbol = "DSHAER11"
        elif category == Catlmk.FLAGSTAFF_FLAGPOLE:
            symbol = "FLGSTF01"
        elif category == Catlmk.FLARE_STACK:
            symbol = pick("FLASTK11", "FLASTK01")
        elif category == Catlmk.MAST:
            symbol = pick("MSTCON14", "MSTCON04")
        elif category == Catlmk.MONUMENT:
            symbol = "MONUMT12"
        elif category in (Catlmk.COLUMN_PILLAR, Catlmk.OBELISK, Catlmk.STATUE):
            symbol = "MONUMT12"
        elif category == Catlmk.CROSS:
            symbol = pick("BUIREL13", "BUIREL01")
        elif category == Catlmk.DOME:
            symbol = pick("DOMES011", "DOMES001")
        elif category == Catlmk.RADAR_SCANNER:
            symbol = pick("RASCAN11", "RASCAN01")
        elif category == Catlmk.TOWER:
            symbol = pick("TOWERS12", "TOWERS02")
        elif category == Catlmk.WINDMILL:
            symbol = "WNDMIL12"
        elif category == Catlmk.WINDMOTOR:
            symbol = pick("WIMCON11", "WIMCON01")
        else:
            # MEMORIAL_PLAQUE, CEMETERY, WINDSOCK, SPIRE_MINARET, None
            symbol = pick("POSGEN03", "POSGEN01")
        feature.point_symbol(symbol)

    def layers(self, b):
        return [
            b.area_layer_with_fill_color(Color.CHBRN, None),
            b.area_layer_with_single_symbol(),
            b.line_layer_with_colors(LINE_COLORS, width=1.0),
            b.point_layer_from_symbol(),
        ]
