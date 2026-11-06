"""Light sector icons: the arc a sector light is drawn with.

The icon is named by the ``SI`` prop that ``lights`` writes
(``sector_<s1>_<s2>_<day>_<dusk>_<night>_<dayLine>_<duskLine>_<nightLine>_<r>``) and rendered
into the sprite sheet at conversion time.
"""

import math
from dataclasses import dataclass

from .colors import ThemeMode

CENTER = "100.0"


def build_sector_svg(sectr1, sectr2, fill_color, line_color, radius):
    """A 200×200 SVG of the light sector between bearings ``sectr1`` and ``sectr2``.

    The arc (or a full circle when the bearings coincide) is drawn in ``fill_color``, with
    dashed sector legs in ``line_color``. S-57 bearings are from seaward towards the light, so
    both are reversed (+180°).
    """
    sector1 = (sectr1 + 180.0) % 360.0
    sector2 = (sectr2 + 180.0) % 360.0
    cx = cy = 100.0
    a1 = sector1 * math.pi / 180.0
    a2 = sector2 * math.pi / 180.0
    x1 = cx + radius * math.sin(a1)
    y1 = cy - radius * math.cos(a1)
    x2 = cx + radius * math.sin(a2)
    y2 = cy - radius * math.cos(a2)

    r = _fmt(radius)
    span = (sector2 - sector1 + 360.0) % 360.0
    if span == 0.0:
        arc = f'<circle cx="{CENTER}" cy="{CENTER}" r="{r}" fill="none" stroke="{fill_color}" stroke-width="4"/>'
    else:
        large_arc = 1 if span > 180.0 else 0
        arc = (
            f'<path d="M {_fmt(x1)} {_fmt(y1)} A {r} {r} 0 {large_arc} 1 {_fmt(x2)} {_fmt(y2)}"\n'
            f'      fill="none" stroke="{fill_color}" stroke-width="4" stroke-linecap="butt"/>'
        )

    if span == 0.0:
        legs = ""
    else:

        def line(x, y):
            return (
                f'<line x1="{CENTER}" y1="{CENTER}" x2="{_fmt(x)}" y2="{_fmt(y)}"\n'
                f'        stroke="{line_color}" stroke-width="2"\n'
                f'        stroke-dasharray="4 6" stroke-linecap="butt"/>'
            )

        legs = f"  {line(x1, y1)}\n  {line(x2, y2)}"

    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">\n  {arc}\n  {legs}\n</svg>'


def _fmt(x):
    tenths = int(round(x * 10.0))
    return f"{int(tenths / 10)}.{abs(tenths) % 10}"


@dataclass(frozen=True)
class SectorIcon:
    """A parsed ``SI`` icon name."""

    name: str
    sectr1: float
    sectr2: float
    fill: dict
    line: dict
    radius: float

    @staticmethod
    def parse(name):
        if not name.startswith("sector_"):
            return None
        parts = name[len("sector_") :].split("_")
        if len(parts) < 9:
            return None
        modes = [ThemeMode.DAY, ThemeMode.DUSK, ThemeMode.NIGHT]
        return SectorIcon(
            name=name,
            sectr1=float(parts[0]),
            sectr2=float(parts[1]),
            fill=dict(zip(modes, parts[2:5])),
            line=dict(zip(modes, parts[5:8])),
            radius=float(parts[8]),
        )

    def svg(self, mode):
        return build_sector_svg(self.sectr1, self.sectr2, self.fill[mode], self.line[mode], self.radius)
