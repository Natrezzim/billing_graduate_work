from functools import lru_cache

from fastapi import Depends

from db.postgres import AsyncSession, get_session
from models.billing_models import PaymentStatus


class PaymentStatusService:
    def __init__(self, storage: AsyncSession):
        self.storage = storage

    async def payment_status(self, response):
        data = PaymentStatus(
            id=response['object']['id'],
            event=response['event'],
            status=response['object']['status'],
            description=response['object']['description'],
            created_at=response['object']['created_at'],
            user_id=response['object']['metadata']['user_id']
        )

        self.storage.add(data)
        await self.storage.commit()
        await self.storage.refresh(data)

        return data


@lru_cache()
def get_payments_status_service(storage: AsyncSession = Depends(get_session)) -> PaymentStatusService:
    return PaymentStatusService(storage)
