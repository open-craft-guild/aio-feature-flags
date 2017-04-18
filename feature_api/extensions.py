import aiomysql
from sqlalchemy.sql import select

from db.models import FeatureFlag
from .app import _logger

async def get_flags(conn):
    flags = await conn.execute(
        select([FeatureFlag.__table__])
    )
    if not flags:
        return "Sorry, list is empty"
    result = await flags.fetchall()
    return result


async def set_flag(conn, name, is_active):
    trans = await conn.begin()
    try:
        flag_id = await conn.execute(
            FeatureFlag.__table__.insert().values(name=name,
                                                  is_active=is_active)
        )
    except Exception:
        _logger.exeption()
        trans.rollback()
        raise RuntimeError
    else:
        await trans.commit()