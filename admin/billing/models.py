import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(_('username'), max_length=50,
                                db_index=True)
    cart = models.JSONField(_('cart'))
    payment_system = models.CharField(_('payment system'), max_length=20,
                                db_index=True)
    payment_status = models.CharField(_('payment status'), max_length=50)
    paid = models.BooleanField(_('paid'))
    created_at = models.DateTimeField(_('created at'))
    updated_at = models.DateTimeField(_('updated at'))

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
        db_table = "admin\".\"payment"

    def __str__(self):
        return f'{self.payment_system}::{self.id}'
