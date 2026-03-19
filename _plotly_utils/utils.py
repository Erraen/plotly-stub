"""Stub for _plotly_utils.utils.

Required by dash/background_callback/managers/celery_manager.py:
    from _plotly_utils.utils import PlotlyJSONEncoder
"""

import json


class PlotlyJSONEncoder(json.JSONEncoder):
    pass
