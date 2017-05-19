"""Collection of HTTP helpers."""

from functools import partial, wraps
from inspect import iscoroutine

from aiohttp.web import (
    json_response, HTTPError,
    HTTPSuccessful, HTTPRedirection
)


def async_json_out(orig_method=None, *, status=200, content_type='application/json', **dec_kwargs):
    """Turn dict output of an HTTP handler into JSON response.

    Decorates aiohttp request handlers.
    """
    if orig_method is None:
        return partial(async_json_out, status=200, content_type='application/json', **dec_kwargs)

    @wraps(orig_method)
    async def wrapper(*args, **kwargs):
        try:
            dict_resp = orig_method(*args, **kwargs)

            if iscoroutine(dict_resp):
                dict_resp = await dict_resp
        except (HTTPSuccessful, HTTPRedirection):
            raise
        except HTTPError as he:
            if he.empty_body:
                raise

            status = he.status_code,
            dict_resp = {
                'error': he.body,
            }

        try:
            status = dict_resp['status']
        except KeyError:
            dict_resp['status'] = status

        return json_response(
            dict_resp,
            status=status,
            content_type=content_type,
            **dec_kwargs
        )
    return wrapper
