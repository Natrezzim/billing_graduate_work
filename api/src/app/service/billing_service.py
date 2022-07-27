from functools import lru_cache

from fastapi import Depends

from app.db.postgres import AsyncSession, get_session
from app.models.billing_models import Payments, PaymentsCreate


class PaymentsService:
    def __init__(self, storage: AsyncSession):
        self.storage = storage

    async def payment_create(self, payment_data: PaymentsCreate, payment):
        yookassa_response = payment
        payment_data = Payments(
            currency=payment_data.currency,
            value=payment_data.value,
            description=yookassa_response.description,
            created_at=yookassa_response.created_at,
            payment_id=yookassa_response.id,
            user_id=payment_data.user_id
        )
        self.storage.add(payment_data)
        await self.storage.commit()
        await self.storage.refresh(payment_data)

        return {'status': yookassa_response.status,
                'confirmation_url': yookassa_response.confirmation.confirmation_url,
                'return_url': yookassa_response.confirmation.return_url}


@lru_cache()
def get_payments_service(storage: AsyncSession = Depends(get_session)) -> PaymentsService:
    return PaymentsService(storage)
