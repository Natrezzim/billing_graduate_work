import uuid

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from yookassa import Payment

from app.service.auth_service import Auth
from app.models.billing_models import PaymentsCreate
from app.service.billing_service import PaymentsService, get_payments_service

router = APIRouter()
auth_handler = Auth()
security = HTTPBearer()


@router.get('/payment')
async def get_payments(credentials: HTTPBasicCredentials = Depends(security)):
    '''
    Получить список последних 10 платежей
    '''
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    params = {'limit': 10}
    payment_list = Payment.list(params)
    return payment_list


@router.get('/payment/{payment_id}')
async def get_payment_by_id(payment_id: str,
                            credentials: HTTPBasicCredentials = Depends(security)):
    '''
    Получить платеж по payment_id
    '''
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)

    payment = Payment.find_one(payment_id)
    return payment


@router.post('/payment')
async def transaction_test(payment_data: PaymentsCreate,
                           transaction: PaymentsService = Depends(get_payments_service),
                           credentials: HTTPBasicCredentials = Depends(security)):

    token = credentials.credentials
    user_id = auth_handler.decode_token(token)

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
            "return_url": "http://moviesbilling.ddns.net/return-url"
        },
        "metadata": {
            "user_id": user_id
        },
        "description": payment_data.description}, idempotence_key)

    transaction = await transaction.payment_create(payment_data, payment)
    return transaction
