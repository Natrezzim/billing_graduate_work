import logging
import time
from http import HTTPStatus

from app.db.repository import SyncRepository
from app.service.sync import SYNCHRONIZERS

REPOSITORY = SyncRepository()
LOGGER = logging.getLogger(__name__)


async def sync():
    base_sleep = sleep = 3
    all_data = await REPOSITORY.get_sync_data()
    for data, synchronizer in zip(all_data, SYNCHRONIZERS):
        while True:
            status, result = await synchronizer.send_data(data)
            if status == HTTPStatus.CREATED:
                sleep = base_sleep
                break

            LOGGER.exception(f'{synchronizer.__class__.__name__}::{status}::{result}')
            time.sleep(sleep)
            sleep *= 2
            continue
