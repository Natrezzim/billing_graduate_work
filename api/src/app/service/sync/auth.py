from app.core.config import Settings
from app.service.sync.base import BaseSynchronizer


class AuthSynchronizer(BaseSynchronizer):
    url = f'{Settings.auth_url}{Settings.auth_sync_path}'
    auth = Settings.auth_token
