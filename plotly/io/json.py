"""Stub for plotly.io.json.

Required by dash/_utils.py to_json():
    from plotly.io.json import to_json_plotly

The original handles plotly-specific types (Figure, numpy, pandas, datetime,
Decimal, PIL). Dash calls to_json() in three places:
  1. serve_layout(layout)    — Dash component tree (Component objects)
  2. _generate_config_html() — plain dict
  3. dependencies()          — list of dicts

For (1) it's critical: Component.to_plotly_json() only converts the top-level
object, nested components remain as objects — orjson will raise TypeError.
Hence the default handler is required.
"""

from __future__ import annotations

from typing import Any

import orjson


def to_json_plotly(v: Any, pretty: bool = False, engine: str | None = None) -> str:
    def _default(obj: Any) -> Any:
        # Dash Component -> dict via to_plotly_json()
        if hasattr(obj, "to_plotly_json"):
            return obj.to_plotly_json()
        # datetime/date -> ISO string
        if hasattr(obj, "isoformat"):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    # Convert top-level object (same as the original)
    if hasattr(v, "to_plotly_json"):
        v = v.to_plotly_json()

    opts = orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY
    if pretty:
        opts |= orjson.OPT_INDENT_2

    result = orjson.dumps(v, default=_default, option=opts).decode()

    # HTML-escape for safe embedding in <script> tags
    return result.replace("</", "<\\/")
