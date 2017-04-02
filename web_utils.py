from functools import partial, wraps

from aiohttp.web import json_response


def async_json_out(orig_method=None, *, content_type='application/json', **kwargs):
    if orig_method is None:
        return partial(async_json_out, content_type='application/json', **kwargs)

    @wraps(orig_method)
    async def wrapper(request):
        dict_resp = await orig_method(request)
        return json_response(
            dict_resp,
            content_type=content_type,
            **kwargs
        )
    return wrapper
