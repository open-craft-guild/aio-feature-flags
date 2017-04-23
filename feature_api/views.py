"""HTTP handlers declarations."""

import logging

from aiohttp.web_urldispatcher import View

from web_utils import async_json_out

from . import extensions

_logger = logging.getLogger(__name__)


class Flag(View):
    """Feature flag endpoint."""

    @async_json_out
    async def get(self):
        """React for GET request."""
        async with self.request.app['db_engine'].acquire() as conn:
            flags = await extensions.get_flags(conn)
            return {'items': flags}

    @async_json_out
    async def post(self):
        """React for POST request."""
        async with self.request.app['db_engine'].acquire() as conn:
            data = await self.request.post()
            try:
                name = data['name']
                is_active = data['is_active']
                await extensions.set_flag(conn, name, bool(is_active))
            except KeyError:
                _logger.exception('Invalid key parameter.')
                return {'info': 'One or more required params is not specified'}
            except RuntimeError:
                _logger.exception('Error while writing to DB.')
                return {'info': "Sorry, there's error while writing to db."}
            else:
                return {'info': 'success'}


class GetOneFlag(View):
    """Work with only one flag not a sequence."""

    @async_json_out
    async def get(self):
        """React for GET request."""
        async with self.request.app['db_engine'].acquire() as conn:
            name = self.request.match_info['name']
            try:
                flag = await extensions.get_flag_by_name(conn, name)
            except KeyError:
                _logger.exception('Invalid key parameter.')
                return {'info': 'No id parameter specified.'}
            except FileNotFoundError:
                return {'info': 'No flag found'}
            else:
                return {'flag': flag}

    @async_json_out
    async def delete(self):
        name = self.request.match_info['name']

        if not name:
            return {'info': 'item is not in db'}

        async with self.request.app['db_engine'].acquire() as conn:
            result = await extensions.delete(conn, name)
            return {'info': result}

    @async_json_out
    async def patch(self):
        name = self.request.match_info['name']
        data = await self.request.post()

        if not name:
            return {'info': 'item is not in db'}

        async with self.request.app['db_engine'].acquire() as conn:
            result = await extensions.update(conn, name, bool(data['is_active']))
            return {'info': result}
