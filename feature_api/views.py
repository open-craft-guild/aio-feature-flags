"""HTTP handlers declarations."""

from aiohttp.web_urldispatcher import View

from web_utils import async_json_out


from . import extensions

class Index(View):
    """Dummy index endpoint."""

    @async_json_out
    async def get(self):
        """Return dummy json in response to HTTP GET request."""
        return {'content': 'feature-flags-api'}


class Flag(View):
    """Feature flag endpoint."""

    @async_json_out
    async def get(self):
        """React for GET request."""
        async with self.request.app['db_engine'].acquire() as conn:
            flags = await extensions.get_flags(conn)
            return {'items': str(flags)}

    @async_json_out
    async def post(self):
        """React for POST request."""
        async with self.request.app['db_engine'].acquire() as conn:
            data = await self.request.post()
            try:
                name = data['name']
                is_active = data['is_active']
            except KeyError:
                return {'info': 'One or more required params is not specified'}
            await extensions.set_flag(conn, name, bool(is_active))
            return {'info': 'success'}
