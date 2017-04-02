import asyncio
import logging

from aio_manager import Manager
from aio_manager.commands.ext import sqlalchemy

from feature_api.app import build_application

async def main():
    logging.basicConfig(level=logging.WARNING)

    app = await build_application()
    manager = Manager(app)

    sqlalchemy.configure_manager(
        manager, app, app['declarative_base'],
        url='mysql+pymysql://{usr}:{pwd}@{host}:{port}/{db}'.
            format(
                usr=app.config['DATABASE_USERNAME'],
                pwd=app.config['DATABASE_PASSWORD'],
                db=app.config['DATABASE_NAME'],
                host=app.config['DATABASE_HOST'],
                port=app.config['DATABASE_PORT']
             )
    )
    return manager
