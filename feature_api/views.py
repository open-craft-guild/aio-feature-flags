"""HTTP handlers declarations."""

import logging

import aiohttp.web as web
from aiohttp.web_urldispatcher import View

from web_utils import async_json_out

from . import data_access

_logger = logging.getLogger(__name__)


class Flag(View):
    """Feature flag endpoint."""

    @async_json_out
    async def get(self):
        """Return list of existed flags."""
        async with self.request.app['db_engine'].acquire() as conn:
            flags = await data_access.get_flags(conn)
        return {'items': flags, 'status_code': 200}

    @async_json_out
    async def post(self):
        """Create new flag."""
        try:
            data = await self.request.post()
            name = data['name']
            is_active = data['is_active']
            async with self.request.app['db_engine'].acquire() as conn:
                result = await data_access.set_flag(conn, name, bool(is_active))
        except KeyError:
            _logger.exception('Missing key parameter.')
            return {'status_code': 400}
        except RuntimeError:
            _logger.exception('Error while writing to DB.')
            return {'status_code': 403}
        else:
            return result


class GetOneFlag(View):
    """Work with only one flag not a sequence."""

    @async_json_out
    async def get(self):
        """Return flag by given name."""
        try:
            name = self.request.match_info['name']
            async with self.request.app['db_engine'].acquire() as conn:
                flag = await data_access.get_flag_by_name(conn, name)
        except KeyError:
            _logger.exception('Missing key parameter.')
            return {'status_code': 400}
        except web.HTTPNotFound:
            return {'status_code': 404}
        else:
            return flag

    @async_json_out
    async def delete(self):
        try:
            name = self.request.match_info['name']
            async with self.request.app['db_engine'].acquire() as conn:
                result = await data_access.delete(conn, name)
        except KeyError:
            _logger.exception('Missing key parameter.')
            return {'status_code': 404}
        else:
            return result

    @async_json_out
    async def patch(self):
        try:
            data = await self.request.post()
            name = self.request.match_info['name']
            is_active = data['is_active']
            async with self.request.app['db_engine'].acquire() as conn:
                result = await data_access.update(conn, name, bool(is_active))
        except KeyError:
            _logger.exception('Missing key parameter.')
            return {'status_code': 404}
        else:
            return result
