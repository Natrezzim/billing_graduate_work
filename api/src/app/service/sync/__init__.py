from app.service.sync.admin import AdminSynchronizer
from app.service.sync.auth import AuthSynchronizer

SYNCHRONIZERS = (AdminSynchronizer(), AuthSynchronizer())

__all__ = ('SYNCHRONIZERS', 'AdminSynchronizer', 'AuthSynchronizer')
