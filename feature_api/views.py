"""HTTP handlers declarations."""

import logging

import aiohttp.web as web
from aiohttp.web_urldispatcher import View

from web_utils import async_json_out

from . import data_access

_logger = logging.getLogger(__name__)


class FeatureFlagsCollection(View):
    """Feature flag endpoint."""

    @async_json_out(status=200)  # Ok
    async def get(self):
        """Return list of existed flags."""
        async with self.request.app['db_engine'].acquire() as conn:
            flags = await data_access.get_flags(conn)
        return {'items': flags}

    @async_json_out(status=201)  # Created
    async def post(self):
        """Create new flag."""
        try:
            data = await self.request.post()
            name = data['name']
            is_active = data['is_active']
            async with self.request.app['db_engine'].acquire() as conn:
                result = await data_access.set_flag(conn, name, bool(is_active))
        except KeyError as ke:
            err_msg = 'Missing key parameter.'
            _logger.exception(err_msg)
            raise web.HTTPBadRequest(body=err_msg) from ke  # 400 Bad Request status built-in
        except RuntimeError as re:  # FIXME: consider moving handling of such errors to decorator
            err_msg = 'Error while writing to DB.'
            _logger.exception(err_msg)
            raise web.HTTPInternalServerError(body=err_msg) from re  # 500 Internal Server Error embedded
        else:
            return result


class FeatureFlag(View):
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
        data = await self.request.post()
        name = self.request.match_info['name']
        is_active = data.get('is_active')
        if is_active is None:
            return {'status_code': 404}

        async with self.request.app['db_engine'].acquire() as conn:
            result = await data_access.update(conn, name, bool(is_active))

        return result
