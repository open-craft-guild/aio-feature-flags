import logging
from sqlalchemy.sql import select
from sqlalchemy import exc

from db.models import FeatureFlag

_logger = logging.getLogger(__name__)

async def get_flags(conn):
    flags = await conn.execute(
        select([FeatureFlag.__table__])
    )
    if not flags:
        return "Sorry, list is empty"
    result = await flags.fetchall()
    return [{'id': i['id'],
             'name': i['name'],
             'is_active': i['is_active']} for i in result]


async def set_flag(conn, name, is_active):
    async with conn.begin() as trans:
        try:
            await conn.execute(FeatureFlag.__table__
                               .insert().values(name=name,
                                                is_active=is_active))
        except exc:
            _logger.exception('Transaction failed.')
            trans.rollback()
            raise RuntimeError
        else:
            await trans.commit()

async def get_flag_by_name(conn, name):
    try:
        flag = await conn.execute(
            select([FeatureFlag.__table__]).where(FeatureFlag.name == name)
        )
        result = await flag.fetchone()
        if result is None:
            raise Exception
    except Exception:
        _logger.exception('Failed while get info from DB.')
        raise FileNotFoundError
    else:
        return {'id': result['id'],
                'name': result['name'],
                'is_active': result['is_active']}

async def update_flag(conn, name):
    return None
