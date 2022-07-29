from app.core.config import get_settings
from app.service.sync.base import BaseSynchronizer

settings = get_settings()


class AdminSynchronizer(BaseSynchronizer):
    url = f'{settings.admin_url}{settings.admin_sync_path}'
    auth = (settings.admin_login, settings.admin_password)
