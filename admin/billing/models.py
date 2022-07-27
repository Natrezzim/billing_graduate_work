import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(_('username'), max_length=50,
                                db_index=True)
    cart = models.ManyToManyField('product', related_name='payments',
                                  verbose_name=_('cart'))
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


class Product(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('product name'), max_length=50)
    value = models.FloatField(_('product price'), default=0.0,
                              validators=[MinValueValidator(0.0)])
    currency = models.CharField(_('product currency'), max_length=5)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        db_table = "admin\".\"product"

    def __str__(self):
        return f'{self.name}: {self.value} {self.currency}'
