from app.core.config import get_settings
from app.service.sync.base import BaseSynchronizer

settings = get_settings()


class AuthSynchronizer(BaseSynchronizer):
    url = f'{settings.auth_url}{settings.auth_sync_path}'
    auth = None
