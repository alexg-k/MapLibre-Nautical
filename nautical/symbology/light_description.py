"""The light description text string, e.g. ``Fl(2) R 6s7.6m5M``.

Built per S-52 PresLib 4.0 Part I §10.6.3 "Light Description Text Strings". Attributes are output
in the spec's draw order: CATLIT, LITCHR, SIGGRP, COLOUR, SIGPER, HEIGHT, VALNMR, STATUS.

HEIGHT is deliberately not rendered here: the string is split into a ``head`` (everything up to
and including the period) and a ``tail`` (range and status), and the style splices the height
between them in the viewer's units.
"""

from dataclasses import dataclass

from .number import double_to_string, round_half_even
from .props import double_value, int_value, int_values, string_value

CATLIT = {1: "Dir", 5: "Aero", 7: "Fog Det Lt"}

LITCHR = {
    1: "F",
    2: "Fl",
    3: "LFl",
    4: "Q",
    5: "VQ",
    6: "UQ",
    7: "Iso",
    8: "Oc",
    9: "IQ",
    10: "IVQ",
    11: "IUQ",
    12: "Mo",
    13: "FFl",
    14: "Fl+LFl",
    15: "OcFl",
    16: "FLFl",
    17: "AlOc",
    18: "AlLFl",
    19: "AlFl",
    20: "Al",
    25: "Q+LFl",
    26: "VQ+LFl",
    27: "UQ+LFl",
    28: "Al",
    29: "AlF Fl",
}

COLOUR = {1: "W", 3: "R", 4: "G", 5: "Bu", 6: "Y", 9: "Am", 10: "Vi", 11: "Or"}

STATUS = {2: "occas", 7: "temp", 8: "priv", 11: "exting", 17: "U"}


@dataclass(frozen=True)
class LightDescription:
    head: str
    tail: str

    @staticmethod
    def of(props):
        """``None`` when the light has no characteristic."""
        litchr = int_value(props, "LITCHR")
        characteristic = LITCHR.get(litchr) if litchr is not None else None
        if characteristic is None:
            return None

        category = _join(props, "CATLIT", CATLIT, " ")
        group = string_value(props, "SIGGRP") or ""
        if _is_default_group(group):
            group = ""
        colour = _join(props, "COLOUR", COLOUR, "")
        status = _join(props, "STATUS", STATUS, " ")

        period = _positive(props, "SIGPER")
        period = f"{format_number(period)}s" if period is not None else ""
        range_ = _positive(props, "VALNMR")
        range_ = f"{format_number(range_)}M" if range_ is not None else ""
        has_height = _positive(props, "HEIGHT") is not None
        has_numbers = bool(period) or has_height or bool(range_)

        head = " ".join(s for s in [category, f"{characteristic}{group}", colour] if s)
        if has_numbers:
            head += " "
        head += period
        tail = range_ if not status else f"{range_} {status}"
        return LightDescription(head, tail)


def _join(props, key, table, sep):
    return sep.join(s for s in (table.get(i) for i in int_values(props, key)) if s is not None)


def _positive(props, key):
    v = double_value(props, key)
    return v if v is not None and v > 0.0 else None


def _is_default_group(group):
    return not group.replace("()", "").replace("(1)", "").strip()


def format_number(value):
    """A period, height or range to at most one decimal place, ties to even."""
    tenths = round_half_even(value * 10.0) / 10.0
    if tenths == float(int(tenths)):
        return str(int(tenths))
    return double_to_string(tenths)
