"""Typed reads of S-57 feature props, with lenient parsing.

A value is read through its JSON primitive text, so the string ``"3"`` reads as the integer 3
while the real ``3.0`` does not, and GDAL's list attributes arrive as lists of strings
(``"COLOUR": ["1", "3"]``).

A list where a scalar is expected, or a scalar where a list is expected, answers ``None``.
"""

import math
import struct


def _content(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, str):
        return v
    if isinstance(v, (int, float)):
        return _number_text(v)
    return None


def _number_text(n):
    if isinstance(n, int):
        return str(n)
    if math.isnan(n) or math.isinf(n):
        return None
    if n == int(n) and abs(n) < 1e16:
        return f"{n:.1f}"
    return repr(n)


def _content_or_null_text(v):
    if v is None:
        return "null"
    if isinstance(v, (list, dict)):
        return None
    return _content(v)


def to_int(s):
    """A decimal ``i32`` as Rust parses it: optional sign, digits only."""
    if s is None:
        return None
    t = s[1:] if s[:1] in "+-" else s
    if not t.isdigit() or not t.isascii():
        return None
    value = int(s)
    if -(2**31) <= value < 2**31:
        return value
    return None


def to_number(s):
    """The decimal forms S-57 values take, ``None`` for anything else (including ``inf``)."""
    if s is None or s != s.strip() or "_" in s or s.lower() in ("inf", "infinity", "+inf", "-inf"):
        return None
    try:
        value = float(s)
    except ValueError:
        return None
    if math.isinf(value):
        return None
    return value


def as_f32(x):
    """``x`` rounded to single precision, the width njord compares depths in."""
    return struct.unpack("f", struct.pack("f", x))[0]


def string_value(props, key):
    return _content(props.get(key))


def int_value(props, key):
    return to_int(string_value(props, key))


def float_value(props, key):
    """A depth or height as an ``f32``."""
    v = to_number(string_value(props, key))
    return None if v is None else as_f32(v)


def double_value(props, key):
    return to_number(string_value(props, key))


def string_values(props, key):
    """The elements of a list attribute as text, ``None`` when absent or not a list."""
    v = props.get(key)
    if not isinstance(v, list):
        return None
    out = []
    for item in v:
        text = _content_or_null_text(item)
        if text is None:
            return None
        out.append(text)
    return out


def int_values(props, key):
    """The integer elements of a list attribute; elements that are not integers are dropped."""
    values = string_values(props, key) or []
    return [i for i in (to_int(s) for s in values) if i is not None]
