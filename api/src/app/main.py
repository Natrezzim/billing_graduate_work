import logging
import os
from pathlib import Path

import uvicorn
from app.core.config import Settings
from app.custom_logging import CustomizeLogger
from app.db.pg_db import test_connection
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

settings = Settings()

logger = logging.getLogger(__name__)

config_path = Path(__file__).with_name("logging_config.json")


def create_app() -> FastAPI:
    """

    :return: app
    """
    app = FastAPI(
        title=f'{settings.project_name}',
        docs_url='/app/openapi',
        openapi_url='/app/openapi.json',
        default_response_class=ORJSONResponse,
        description='Сервис приема платежей',
        version='1.0.0',
    )
    logger = CustomizeLogger.make_logger(config_path)
    app.logger = logger
    os.system('./migrations/alembic upgrade head')

    return app


app = create_app()


@app.on_event('startup')
async def startup():
    await test_connection()
    logger.info("UP app")


@app.on_event('shutdown')
async def shutdown() -> None:
    logger.info("Shutdown app")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)  # noqa S104
