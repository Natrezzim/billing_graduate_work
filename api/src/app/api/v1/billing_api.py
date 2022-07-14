import uuid

from app.models.billing_models import PaymentsCreate
from app.service.billing_service import PaymentsService, get_payments_service
from fastapi import APIRouter, Depends
from yookassa import Payment

router = APIRouter()


@router.post('/payment')
async def transaction_test(payment_data: PaymentsCreate,
                           transaction: PaymentsService = Depends(get_payments_service)):
    idempotence_key = str(uuid.uuid4())
    payment_data.payment_id = idempotence_key

    payment = Payment.create({
        "amount": {
            "value": payment_data.value,
            "currency": payment_data.currency
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://127.0.0.1:8000/return-url"
        },
        "metadata": {
            "idempotence_key": idempotence_key
        },
        "description": payment_data.description}, idempotence_key)

    transaction = await transaction.payment_create(payment_data, payment)
    return transaction
