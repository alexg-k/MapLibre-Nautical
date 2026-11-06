"""Debug tile overlay, registered only with ``SymbologyConfig.debug_tile``."""

from .prelude import *


class Debug(Layerable):
    def layers(self, b):
        return [
            b.layer(
                "debug-msg",
                LayerType.SYMBOL,
                filter=["any", filters.eq_type_point()],
                layout=layout(
                    text_font=[Font.ROBOTO_BOLD],
                    text_anchor=Anchor.CENTER,
                    text_justify=TextJustify.CENTER,
                    text_field=["get", "DMSG"],
                    text_allow_overlap=True,
                    text_ignore_placement=True,
                    text_size=11.0,
                    symbol_placement=Placement.POINT,
                ),
            ),
            b.layer(
                "debug-line",
                LayerType.LINE,
                filter=[filters.ALL, filters.eq_type_line_string()],
                paint=paint(line_color=b.color(Color.CSTLN), line_width=5.0),
            ),
        ]
