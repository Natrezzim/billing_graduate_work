import logging

from app.utils.task_manager import TaskManager

logger = logging.getLogger(__name__)

tm = TaskManager()

logger.info('STARTING TASK MANAGER')

tm.run()
