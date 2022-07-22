from yookassa import Webhook
from fastapi import APIRouter, Request, Depends
from app.service.webhook_service import PaymentStatusService, get_payments_status_service

router = APIRouter()


@router.post('/notification-url', status_code=200)
async def post_notification_url(request: Request,
                                status_service: PaymentStatusService = Depends(get_payments_status_service)):
    """
    URL для получения уведомлений
    """
    response = await request.json()
    status = await status_service.payment_status(response)
    return {'response': 200}


@router.get('/webhook-list')
async def webhook_list():
    """
    Список доступных подписок на события
    """
    list = Webhook.list()
    return list


@router.get('/webhook-remove/{webhook_id}')
async def remove_webhook(webhook_id):
    """
    Удалить подписку по ID
    """
    response = Webhook.remove(webhook_id)
    return {'message', f'Webhook {webhook_id} removed'}
