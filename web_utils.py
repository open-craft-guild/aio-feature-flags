"""Collection of HTTP helpers."""

from functools import partial, wraps
from inspect import iscoroutine

from aiohttp.web import json_response


def async_json_out(orig_method=None, *, status=200, content_type='application/json', **kwargs):
    """Turn dict output of an HTTP handler into JSON response.

    Decorates aiohttp request handlers.
    """
    if orig_method is None:
        return partial(async_json_out, status=200, content_type='application/json', **kwargs)

    @wraps(orig_method)
    async def wrapper(*args, **kwargs):
        dict_resp = orig_method(*args, **kwargs)

        if iscoroutine(dict_resp):
            dict_resp = await dict_resp

        return json_response(
            dict_resp,
            status=status,
            content_type=content_type,
            **kwargs
        )
    return wrapper
