"""The small style-value types the layer helpers take."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Symbol:
    """An icon: a fixed sprite, or the sprite named by a feature prop (``SY``, ``SY2``, ...)."""

    sprite: str | None = None
    number: int | None = None

    @staticmethod
    def of(sprite):
        return Symbol(sprite=sprite)

    @staticmethod
    def prop(number=None):
        return Symbol(number=number)

    def property(self):
        if self.sprite is not None:
            return self.sprite
        if self.number is None:
            return ["get", "SY"]
        return ["get", f"SY{self.number}"]


@dataclass(frozen=True)
class Label:
    """Label text: a literal, or a feature prop."""

    text: str | None = None
    prop: str | None = None

    def property(self):
        return self.text if self.text is not None else ["get", self.prop]


@dataclass(frozen=True)
class IconRot:
    """Icon rotation: fixed degrees, or a feature prop."""

    degrees: float | None = None
    prop: str | None = None

    def property(self):
        return self.degrees if self.degrees is not None else ["get", self.prop]


@dataclass(frozen=True)
class Offset:
    """A fixed ``(x, y)`` offset (positive is right and down), or ``eq`` when the prop ``key``
    equals ``value``, else ``neq``."""

    x: float = 0.0
    y: float = 0.0
    key: str | None = None
    value: str | None = None
    eq: tuple = (0.0, 0.0)
    neq: tuple = (0.0, 0.0)

    @staticmethod
    def coord(x, y):
        return Offset(x=x, y=y)

    @staticmethod
    def eval_eq(key, value, eq, neq):
        return Offset(key=key, value=value, eq=eq, neq=neq)

    def property(self):
        if self.key is None:
            return [self.x, self.y]
        return [
            "case",
            ["==", ["get", self.key], self.value],
            ["literal", [self.eq[0], self.eq[1]]],
            ["literal", [self.neq[0], self.neq[1]]],
        ]


class LineStyle:
    """Line dash style: ``SOLID``, ``DASH_LINE`` (``[1, 2]``) or ``custom_dash(width, gap)``."""

    def __init__(self, dash=None):
        self.dash = dash

    @staticmethod
    def custom_dash(width, gap):
        return LineStyle([width, gap])

    def line_dash_array(self):
        return None if self.dash is None else list(self.dash)


LineStyle.SOLID = LineStyle()
LineStyle.DASH_LINE = LineStyle([1.0, 2.0])
