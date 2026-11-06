"""Assembly of the full MapLibre style document."""


def style(factory, depth, theme, sources, sprite, glyphs, name=None):
    """The style for one depth unit and theme.

    ``sources`` is the style's ``sources`` map; the chart source is ``factory.source``. ``sprite``
    and ``glyphs`` are the URLs (or tileserver-gl-relative paths) of the theme's sprite sheet and
    the fonts.
    """
    return {
        "version": 8,
        "name": name or f"{theme.mode.path_name}_simplified",
        "glyphs": glyphs,
        "sprite": sprite,
        "sources": sources,
        "layers": factory.layers(depth, theme),
    }
