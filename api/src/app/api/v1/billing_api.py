import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from yookassa import Payment

from app.core.config import get_settings
from app.core.models import CreatePayment, UpdatePayment, Product
from app.api.v1.schema import CreatePaymentUserRequest
from app.service.auth_service import Auth
from app.service.billing_service import PaymentsService, get_payments_service

settings = get_settings()
router = APIRouter()
auth_handler = Auth()
security = HTTPBearer()


@router.get('/payment')
async def get_payments(credentials: HTTPBasicCredentials = Depends(security),
                       limit: int = Query(settings.payments_limit)):
    '''
    Получить список последних n платежей
    '''
    token = credentials.credentials
    auth_handler.decode_token(token)
    params = {'limit': limit}
    payment_list = Payment.list(params)
    return payment_list


@router.get('/payment/{payment_id}')
async def get_payment_by_id(payment_id: str,
                            credentials: HTTPBasicCredentials = Depends(security)):
    '''
    Получить платеж по payment_id
    '''
    token = credentials.credentials
    auth_handler.decode_token(token)

    payment = Payment.find_one(payment_id)
    return payment


@router.post('/payment')
async def transaction_test(payment_data: CreatePaymentUserRequest,
                           transaction: PaymentsService = Depends(get_payments_service),
                           credentials: HTTPBasicCredentials = Depends(security)):

    user_id = auth_handler.decode_token(credentials.credentials)
    idempotence_key = uuid.uuid4()
    payment = CreatePayment(**payment_data.dict(), idempotence_uuid=idempotence_key, user_id=user_id)
    payment_id = await transaction.payment_create(payment)

    yookassa_payment = Payment.create({
        "amount": {
            "value": sum(item.value for item in payment.products),
            "currency": payment.products[0].currency
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://moviesbilling.ddns.net/return-url"
        },
        "metadata": {
            "user_id": str(user_id),
            "payment_id": str(payment_id)
        },
        "description": payment_data.description}, idempotence_key)
    print("!!!!!!!!!!!!! payment_id", payment_id)
    update_payment = UpdatePayment(id=payment_id, payment_status=yookassa_payment.status, paid=yookassa_payment.paid)

    if await transaction.payment_update(update_payment):

        return {'status': yookassa_payment.status,
                'confirmation_url': yookassa_payment.confirmation.confirmation_url,
                'return_url': yookassa_payment.confirmation.return_url}

    return {}, HTTPStatus.INTERNAL_SERVER_ERROR
