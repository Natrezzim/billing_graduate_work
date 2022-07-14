import logging
from pathlib import Path

import uvicorn
from app.api.v1 import billing_api
from app.core.config import Settings
from app.custom_logging import CustomizeLogger
from app.db.postgres import test_connection, init_db
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from yookassa import Configuration

settings = Settings()

logger = logging.getLogger(__name__)

config_path = Path(__file__).with_name("logging_config.json")

Configuration.account_id = settings.yookassa_account_id
Configuration.secret_key = settings.yookassa_secret_key


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

    return app


app = create_app()


@app.on_event('startup')
async def startup():
    await test_connection()
    await init_db()


@app.on_event('shutdown')
async def shutdown() -> None:
    logger.info("Shutdown app")


app.include_router(billing_api.router, prefix='/api/v1', tags=['payments'])

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)  # noqa S104