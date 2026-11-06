"""S-57 chart symbology and tiling for MapLibre, ported from njord (https://github.com/manimaul/njord).

The package has two halves:

- ``nautical.symbology``: one rule per S-57 object class that (a) adds display props (``SY``,
  ``AC``, ``LC``, ``LP``, ``AP``, ...) to a feature before it is tiled and (b) contributes the
  MapLibre style layers that draw those props.
- ``nautical.tiles``: the conversion pipeline that reads S-57 cells with GDAL, symbolizes the
  features, resolves chart priority and zoom ranges, and feeds tippecanoe.
"""
