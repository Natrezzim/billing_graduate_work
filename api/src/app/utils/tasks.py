import logging
import time
from http import HTTPStatus

from app.core.models import Payments
from app.db.repository.sync import SyncRepository
from app.service.sync import SYNCHRONIZERS

LOGGER = logging.getLogger(__name__)


async def sync():
    repository = SyncRepository()
    base_sleep = sleep = 3
    await repository.set_sync_data()
    for data, synchronizer in zip(repository.all_data, SYNCHRONIZERS):

        while True:
            data = Payments(items=data).dict()
            # status, result = await synchronizer.send_data(data)
            status=201
            if status == HTTPStatus.CREATED:
                sleep = base_sleep
                break

            LOGGER.exception(f'{synchronizer.__class__.__name__}::{status}::{result}')
            time.sleep(sleep)
            sleep *= 2
            continue
    else:
        await repository.set_sync_flag()
