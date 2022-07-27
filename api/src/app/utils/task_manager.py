import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.utils.tasks import sync


class TaskManager:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._scheduler = AsyncIOScheduler()
        self._scheduler.add_job(sync, 'cron', minute='*/3')

    def run(self):
        try:
            self.logger.info('STARTING')
            self._start()
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            self._stop()

    def _start(self):
        if not self._scheduler.running:
            self._scheduler.start()
        asyncio.get_event_loop().run_forever()

    def _stop(self):
        if self._scheduler.running:
            self._scheduler.shutdown()
