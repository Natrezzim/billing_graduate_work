from functools import lru_cache

from fastapi import Depends

# from app.models.billing_models import Payments, PaymentsCreate
from app.core.models import CreatePayment, UpdatePayment
from app.db.repository.payments import PaymentRepository, get_payments_repository


class PaymentsService:
    def __init__(self, repository: PaymentRepository):
        self.repository = repository

    async def payment_update(self, payment_data: UpdatePayment):
        await self.repository.update_payment(payment_data)
        return True

    async def payment_create(self, payment_data: CreatePayment):
        return await self.repository.create_new_payment(payment_data)


@lru_cache()
def get_payments_service(repository: PaymentRepository = Depends(get_payments_repository)) -> PaymentsService:
    return PaymentsService(repository)
