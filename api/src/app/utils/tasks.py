import logging
from asyncio import sleep
from http import HTTPStatus

from app.core.models import Payments
from app.db.repository.sync import SyncRepository
from app.service.sync import SYNCHRONIZERS

LOGGER = logging.getLogger(__name__)


async def sync():
    repository = SyncRepository()
    base_sleep = sleep_time = 3
    await repository.set_sync_data()
    for data, synchronizer in zip(repository.all_data, SYNCHRONIZERS):
        data = Payments(items=data).json()
        while True:
            status, result = await synchronizer.send_data(data)
            if status == HTTPStatus.CREATED:
                sleep_time = base_sleep
                break

            LOGGER.exception(f'{synchronizer.__class__.__name__}::{status}::{result}')
            await sleep(sleep_time)
            sleep_time *= 2
            continue
    else:
        await repository.set_sync_flag()


if __name__ == '__main__':
    from asyncio import get_event_loop
    loop = get_event_loop()
    loop.run_until_complete(sync())
