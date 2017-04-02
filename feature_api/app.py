import asyncio
import os

from aiohttp.web import Application

import aio_yamlconfig
from aiomysql.sa import create_engine

from .config import CONFIG_TRAFARET
from .views import Index

BASE_DIR = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(BASE_DIR, 'config.yaml')


async  def build_application():
    loop = asyncio.get_event_loop()
    app = Application(loop=loop)

    await aio_yamlconfig.setup(app,
                               config_files=[CONFIG_FILE],
                               # trafaret_validator=CONFIG_TRAFARET,
                               base_dir=BASE_DIR)

    app['db_engine'] = await create_engine(
        user=app.config['DATABASE_USERNAME'],
        password=app.config['DATABASE_PASSWORD'],
        db=app.config['DATABASE_NAME'],
        host=app.config['DATABASE_HOST'],
        port=app.config['DATABASE_PORT'],
        echo=True, connect_timeout=5, loop=loop
    )
    # app['declarative_base'] = Base

    app.router.add_route('*', r'/api/v1/', Index.index)

    return app
