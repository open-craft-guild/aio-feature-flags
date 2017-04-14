"""Manager script for running the app and utility tasks."""

import logging

from aio_manager import Manager
from aio_manager.commands.ext import sqlalchemy

from feature_api.app import build_application

_logger = logging.getLogger(__name__)


async def main():
    """Initialize aio_manager instace. It's an entry point function."""
    logging.basicConfig(level=logging.WARNING)

    app = await build_application()
    manager = Manager(app)
    _logger.info('DB Engine configured.')

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
    _logger.info('SQLAlchemy manager extention configured.')
    return manager
