import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart_id = models.UUIDField(default=uuid.uuid4, null=False)
    idempotence_uuid = models.UUIDField(default=uuid.uuid4, null=False)
    description = models.TextField(_('description'), null=False)
    payment_system = models.CharField(_('payment system'), null=False,
                                      max_length=20)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
        db_table = "billing\".\"payment"

    def __str__(self):
        return f'{self.payment_system}::{self.id}'
