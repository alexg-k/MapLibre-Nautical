"""Number formatting and rounding the style JSON and njord's golden fixtures expect.

Numbers print as the shortest decimal that round-trips, always with a fraction (``10.0``), and in
``E`` notation outside ``[1e-3, 1e7)``; :func:`round_half_even` breaks ties to even; :func:`sign`
of zero is zero. Label text written into feature props depends on these exact forms.
"""

import math
from decimal import Decimal


def double_to_string(x):
    """``x`` as the shortest decimal that round-trips, always with a fraction digit."""
    if math.isnan(x):
        return "NaN"
    if math.isinf(x):
        return "Infinity" if x > 0 else "-Infinity"
    magnitude = abs(x)
    if x == 0.0 or 1e-3 <= magnitude < 1e7:
        s = repr(float(x))
        if "e" in s or "E" in s:
            s = format(Decimal(s), "f")
        return s if "." in s else f"{s}.0"
    d = Decimal(repr(float(x)))
    sign, digits, exponent = d.as_tuple()
    digits = list(digits)
    while len(digits) > 1 and digits[-1] == 0:
        digits.pop()
        exponent += 1
    exp = exponent + len(digits) - 1
    mantissa = str(digits[0])
    if len(digits) > 1:
        mantissa += "." + "".join(str(n) for n in digits[1:])
    else:
        mantissa += ".0"
    return f"{'-' if sign else ''}{mantissa}E{exp}"


def round_half_even(x):
    """Rounds to the nearest integer, ties to even."""
    return float(round(x))


def sign(x):
    """``-1.0``, ``1.0`` or, for zero, ``x`` itself."""
    if x > 0.0:
        return 1.0
    if x < 0.0:
        return -1.0
    return x
