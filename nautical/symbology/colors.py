"""S-52 colour tokens, themes, depth units and the ``colors.json`` lookup."""

import json
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class Color(StrEnum):
    NODTA = "NODTA"
    CURSR = "CURSR"
    CHBLK = "CHBLK"
    CHGRD = "CHGRD"
    CHGRF = "CHGRF"
    CHRED = "CHRED"
    CHGRN = "CHGRN"
    CHYLW = "CHYLW"
    CHMGD = "CHMGD"
    CHMGF = "CHMGF"
    CHBRN = "CHBRN"
    CHWHT = "CHWHT"
    SCLBR = "SCLBR"
    CHCOR = "CHCOR"
    LITRD = "LITRD"
    LITGN = "LITGN"
    LITYW = "LITYW"
    ISDNG = "ISDNG"
    DNGHL = "DNGHL"
    TRFCD = "TRFCD"
    TRFCF = "TRFCF"
    LANDA = "LANDA"
    LANDF = "LANDF"
    CSTLN = "CSTLN"
    SNDG1 = "SNDG1"
    SNDG2 = "SNDG2"
    DEPSC = "DEPSC"
    DEPCN = "DEPCN"
    DEPDW = "DEPDW"
    DEPMD = "DEPMD"
    DEPMS = "DEPMS"
    DEPVS = "DEPVS"
    DEPIT = "DEPIT"
    RADHI = "RADHI"
    RADLO = "RADLO"
    ARPAT = "ARPAT"
    NINFO = "NINFO"
    RESBL = "RESBL"
    ADINF = "ADINF"
    RESGR = "RESGR"
    SHIPS = "SHIPS"
    PSTRK = "PSTRK"
    SYTRK = "SYTRK"
    PLRTE = "PLRTE"
    APLRT = "APLRT"
    UINFD = "UINFD"
    UINFF = "UINFF"
    UIBCK = "UIBCK"
    UIAFD = "UIAFD"
    UINFR = "UINFR"
    UINFG = "UINFG"
    UINFO = "UINFO"
    UINFB = "UINFB"
    UINFM = "UINFM"
    UIBDR = "UIBDR"
    UIAFF = "UIAFF"
    OUTLW = "OUTLW"
    OUTLL = "OUTLL"
    RES01 = "RES01"
    RES02 = "RES02"
    RES03 = "RES03"
    BKAJ1 = "BKAJ1"
    BKAJ2 = "BKAJ2"
    MARBL = "MARBL"
    MARCY = "MARCY"
    MARMG = "MARMG"
    MARWH = "MARWH"


class Depth(StrEnum):
    FATHOMS = "fathoms"
    METERS = "meters"
    FEET = "feet"


class ThemeMode(StrEnum):
    """One of the three S-52 colour tables, as ``colors.json`` keys them."""

    DAY = "DAY"
    DUSK = "DUSK"
    NIGHT = "NIGHT"

    @property
    def path_name(self):
        return self.value.lower()


@dataclass(frozen=True)
class Theme:
    """A colour table, optionally overlaid by a named custom set from ``colors.json``."""

    mode: ThemeMode
    custom: str | None = None

    @property
    def name(self):
        return self.mode.path_name if self.custom is None else f"{self.mode.path_name}_{self.custom}"


DAY = Theme(ThemeMode.DAY)
DUSK = Theme(ThemeMode.DUSK)
NIGHT = Theme(ThemeMode.NIGHT)

DEFAULT_COLORS_FILE = Path(__file__).resolve().parent / "data" / "colors.json"


class ColorLibrary:
    """Wraps the parsed ``colors.json``: ``{"library": {MODE: {token: hex}}, "custom": {...}}``."""

    def __init__(self, color_map):
        self.color_map = color_map

    @classmethod
    def load(cls, path=DEFAULT_COLORS_FILE):
        with Path(path).open() as f:
            return cls(json.load(f))

    def color_from(self, color, theme):
        """The hex colour for ``theme``: a custom theme's override, else the mode's colour."""
        if theme.custom is not None:
            override = (
                self.color_map.get("custom", {})
                .get(theme.custom, {})
                .get(theme.mode.value, {})
                .get(color)
            )
            if override is not None:
                return override
        try:
            return self.color_map["library"][theme.mode.value][color]
        except KeyError:
            raise KeyError(f"color key not found {color}") from None

    def colors(self, theme):
        """Every ``(token, hex)`` of ``theme``, in ``colors.json`` order for a built-in mode and
        in :class:`Color` declaration order for a custom theme."""
        if theme.custom is not None:
            return [(color, self.color_from(color, theme)) for color in Color]
        library = self.color_map["library"].get(theme.mode.value, {})
        return [(Color(token), hex_) for token, hex_ in library.items()]

    def has_custom(self, name):
        return name in self.color_map.get("custom", {})

    def custom_names(self):
        return list(self.color_map.get("custom", {}).keys())
