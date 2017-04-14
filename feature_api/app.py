import asyncio
import logging
import os

from aiohttp.web import Application

import aio_yamlconfig
from aiomysql.sa import create_engine

from .config import CONFIG_TRAFARET
from .views import Index
from db.models import Base

BASE_DIR = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(BASE_DIR, 'config.yaml')
_logger = logging.getLogger(__name__)


async def build_application():
    loop = asyncio.get_event_loop()
    app = Application(loop=loop)
    _logger.info('App initialized.')

    await aio_yamlconfig.setup(app,
                               config_files=[CONFIG_FILE],
                               trafaret_validator=CONFIG_TRAFARET,
                               base_dir=BASE_DIR)
    _logger.info('Config loaded.')
    app['db_engine'] = await create_engine(
        user=app.config['DATABASE_USERNAME'],
        password=app.config['DATABASE_PASSWORD'],
        db=app.config['DATABASE_NAME'],
        host=app.config['DATABASE_HOST'],
        port=app.config['DATABASE_PORT'],
        echo=True, connect_timeout=5, loop=loop
    )
    app['declarative_base'] = Base

    app.router.add_route('*', r'/api/v1/features/', Index)
    _logger.info('Routes configured.')

    return app
