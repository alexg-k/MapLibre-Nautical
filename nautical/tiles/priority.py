"""Chart priority and zoom ranges, resolved statically for tippecanoe.

njord assembles each tile at request time: the charts covering the tile are drawn most-detailed
first, a chart only once the zoom reaches its scale's zoom, and every drawn chart's coverage is
subtracted from what the coarser charts may still paint. With pre-built tiles that becomes a
split of every feature into zoom bands:

- a chart's features start at ``max(chart.zoom, MINZ)`` (``MINZ`` is the feature's own SCAMIN);
- wherever a finer chart's coverage overlaps, the feature is cut away from the zoom at which that
  finer chart becomes visible, so the piece inside the overlap gets a ``maxzoom`` one below it.

Tiles are only built up to ``max_zoom``; charts and features that would only appear beyond that
are clamped to it, since MapLibre overzooms the last level.
"""

from dataclasses import dataclass

import shapely
from shapely.ops import unary_union


@dataclass
class Piece:
    """A feature's geometry visible in the zoom band ``[minzoom, maxzoom]`` (``maxzoom`` None: open)."""

    geometry: object
    minzoom: int
    maxzoom: int | None


@dataclass
class ChartPlan:
    chart: object
    zoom: int
    #: ``(threshold_zoom, coverage_added_at_that_zoom)`` in ascending zoom order: the finer
    #: charts that become visible over this one at that zoom.
    thresholds: list


def sort_charts(charts):
    """Most detailed first: by compilation scale, then name."""
    return sorted(charts, key=lambda c: (c.scale, c.name))


def plan(charts, max_zoom):
    """The :class:`ChartPlan` of every chart, in draw order."""
    ordered = sort_charts(charts)
    plans = []
    for i, chart in enumerate(ordered):
        zoom = min(max(chart.zoom, 0), max_zoom)
        by_threshold = {}
        for finer in ordered[:i]:
            if not finer.coverage.intersects(chart.coverage):
                continue
            t = min(max(finer.zoom, 0), max_zoom)
            t = max(t, zoom)
            by_threshold.setdefault(t, []).append(finer.coverage)
        thresholds = []
        for t in sorted(by_threshold):
            union = unary_union(by_threshold[t])
            shapely.prepare(union)
            thresholds.append((t, union))
        plans.append(ChartPlan(chart, zoom, thresholds))
    return plans


def pieces(chart_plan, geometry, props, max_zoom):
    """Splits one feature into the zoom bands it is visible in."""
    minz = chart_plan.zoom
    feature_min = _int(props.get("MINZ"))
    feature_max = _int(props.get("MAXZ"))
    if feature_min is not None:
        minz = max(minz, min(feature_min, max_zoom))
    out = []
    piece = geometry
    for t, added in chart_plan.thresholds:
        if t <= minz:
            # the finer chart is already visible when this feature appears: cut it away outright
            if added.intersects(piece):
                piece = piece.difference(added)
                if piece.is_empty:
                    return _clamp(out, feature_max)
            continue
        if added.intersects(piece):
            out.append(Piece(piece, minz, t - 1))
            piece = piece.difference(added)
            minz = t
            if piece.is_empty:
                return _clamp(out, feature_max)
    out.append(Piece(piece, minz, None))
    return _clamp(out, feature_max)


def _clamp(out, feature_max):
    if feature_max is None:
        return [p for p in out if not p.geometry.is_empty]
    clamped = []
    for p in out:
        if p.geometry.is_empty or p.minzoom > feature_max:
            continue
        maxz = feature_max if p.maxzoom is None else min(p.maxzoom, feature_max)
        clamped.append(Piece(p.geometry, p.minzoom, maxz))
    return clamped


def _int(v):
    if isinstance(v, bool) or v is None:
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None
