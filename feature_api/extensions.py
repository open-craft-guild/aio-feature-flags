import logging
from sqlalchemy import exc

from db.models import FeatureFlag

_logger = logging.getLogger(__name__)

async def get_flags(conn):
    table = FeatureFlag.__table__
    flags = await conn.execute(
        table.select()
    )
    if not flags:
        return "Sorry, list is empty"
    result = await flags.fetchall()
    return [{'id': i['id'],
             'name': i['name'],
             'is_active': i['is_active']} for i in result]


async def set_flag(conn, name, is_active):
    table = FeatureFlag.__table__
    async with conn.begin() as trans:
        try:
            await conn.execute(table
                               .insert().values(name=name,
                                                is_active=is_active))
        except Exception:
            _logger.exception('Transaction failed.')
            trans.rollback()
            raise RuntimeError
        else:
            await trans.commit()

async def get_flag_by_name(conn, name):
    try:
        table = FeatureFlag.__table__
        flag = await conn.execute(
            table.select().where(FeatureFlag.name == name)
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

async def delete(conn, name):
    table = FeatureFlag.__table__
    async with conn.begin():
        await conn.execute(table.
                           delete().
                           where(FeatureFlag.name == name))

        return 'Done'

async def update(conn, name, is_active):
    table = FeatureFlag.__table__
    async with conn.begin():
        await conn.execute(
                table.
                update().
                where(FeatureFlag.name == name).
                values({'is_active': is_active})
        )
        return 'Done'
