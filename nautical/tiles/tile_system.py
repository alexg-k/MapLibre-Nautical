"""Web Mercator scale ↔ zoom math, as njord computes a chart's display zoom."""

import math

EARTH_CIRCUMFERENCE = 40_075_016.686
SCREEN_PIXEL_SIZE_METERS = 0.0254 / 96.0
SCREEN_TILE_SIZE = 256.0

#: What :func:`scale_to_zoom_int` multiplies the fractional zoom by before rounding, so a chart
#: becomes visible slightly before its compilation scale.
TWEAK_ZOOM_TO_SCALE_BY = 0.92


def scale_to_zoom(scale_denominator, latitude_degrees):
    lat_rad = latitude_degrees * math.pi / 180.0
    return math.log2(
        EARTH_CIRCUMFERENCE * math.cos(lat_rad) / (SCREEN_TILE_SIZE * scale_denominator * SCREEN_PIXEL_SIZE_METERS)
    )


def zoom_to_scale(zoom, latitude_degrees):
    lat_rad = latitude_degrees * math.pi / 180.0
    return EARTH_CIRCUMFERENCE * math.cos(lat_rad) / (SCREEN_TILE_SIZE * SCREEN_PIXEL_SIZE_METERS * 2**zoom)


def scale_to_zoom_int(scale_denominator, latitude_degrees, tweak_by=TWEAK_ZOOM_TO_SCALE_BY):
    """:func:`scale_to_zoom` × ``tweak_by``, rounded half to even."""
    if scale_denominator <= 0:
        return 0
    return int(round(scale_to_zoom(scale_denominator, latitude_degrees) * tweak_by))
