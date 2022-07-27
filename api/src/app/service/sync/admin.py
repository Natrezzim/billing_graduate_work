from app.core.config import Settings
from app.service.sync.base import BaseSynchronizer


class AdminSynchronizer(BaseSynchronizer):
    url = f'{Settings.admin_url}{Settings.admin_sync_path}'
    auth = (Settings.admin_login, Settings.admin_password)
