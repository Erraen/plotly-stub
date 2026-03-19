# plotly-stub

Lightweight stub replacement for the [plotly](https://pypi.org/project/plotly/) package.

Provides the minimal interfaces required by [Dash 4.x](https://dash.plotly.com/) so the real plotly (and its heavy dependencies like narwhals) can be excluded from the build.

## Why

Dash depends on `plotly>=5.0.0`, but many Dash apps don't use plotly charts at all (e.g. using uPlot, Chart.js, or other JS charting libraries instead). The real plotly package adds ~18 MB to Nuitka standalone builds and significantly increases build time.

This package declares itself as `plotly==5.999.0`, satisfying Dash's dependency while providing only the stubs Dash actually imports at runtime:

| Dash file | Import | Stub |
|-----------|--------|------|
| `dash/dcc/Graph.py` | `from plotly.graph_objects import Figure` | Empty `Figure` class |
| `dash/dash.py` | `from plotly.offline import get_plotlyjs_version` | Returns `"0.0.0"` |
| `dash/_utils.py` | `from plotly.io.json import to_json_plotly` | orjson-based serializer |
| `dash/background_callback/managers/celery_manager.py` | `from _plotly_utils.utils import PlotlyJSONEncoder` | Bare `json.JSONEncoder` subclass |

## Installation

```bash
pip install plotly @ git+https://github.com/Erraen/plotly-stub.git
```

Or in `requirements.txt`:

```
plotly @ git+https://github.com/Erraen/plotly-stub.git
```

## Usage with Dash

If your Dash app subclasses `dash.Dash`, override `_setup_plotlyjs` to prevent Dash from registering the non-existent `plotly.min.js`:

```python
class App(dash.Dash):
    def _setup_plotlyjs(self) -> None:
        pass
```
