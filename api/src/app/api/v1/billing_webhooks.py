from yookassa import Webhook
from fastapi import APIRouter


router = APIRouter()


@router.get('/notification-url')
async def notification_url():
    """
        URL для получения уведомлений
    """
    return {'message': 'notification url'}


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
