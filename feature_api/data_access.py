import logging

from aiohttp import web

from db.models import FeatureFlag

_logger = logging.getLogger(__name__)
table = FeatureFlag.__table__


async def get_flags(conn):
    flags = await conn.execute(
        table.select()
    )
    result = await flags.fetchall()
    return [{'id': i['id'],
             'name': i['name'],
             'is_active': i['is_active']} for i in result]


async def set_flag(conn, name, is_active):
    async with conn.begin():
        try:
            await conn.execute(table
                               .insert().values(name=name,
                                                is_active=is_active))
        except Exception:
            _logger.exception('Transaction failed.')
            raise RuntimeError
        else:
            return {'status_code': 201}

async def get_flag_by_name(conn, name):
    flag = await conn.execute(
        table.select().where(FeatureFlag.name == name)
    )
    result = await flag.fetchone()
    if result is None:
        _logger.exception('Failed while get info from DB.')
        raise web.HTTPNotFound
    return {'flag': {'id': result['id'],
                     'name': result['name'],
                     'is_active': result['is_active']},
            'status_code': 200}

async def delete(conn, name):
    async with conn.begin():
        await conn.execute(table.
                           delete().
                           where(FeatureFlag.name == name))
    return {'status_code': 200}

async def update(conn, name, is_active):
    async with conn.begin():
        await conn.execute(
                table.
                update().
                where(FeatureFlag.name == name).
                values({'is_active': is_active})
        )
    return {'status_code': 200}
