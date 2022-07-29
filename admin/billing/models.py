import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Product(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('name of product'), max_length=200, db_index=True)
    description = models.TextField(_('description of product'))
    type = models.CharField(_('type of product'), max_length=20)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        db_table = "admin\".\"product"

    def __str__(self):
        return f'{self.name}: {self.type}'


class Price(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='prices', verbose_name='product')
    value = models.FloatField(_('product price'), default=0.0,
                              validators=[MinValueValidator(0.0)])
    currency = models.CharField(_('price currency'), max_length=5)
    description = models.TextField(_('description of price'), blank=False)
    is_active = models.BooleanField(_('is price active'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('price')
        verbose_name_plural = _('prices')
        db_table = "admin\".\"price"

    def __str__(self):
        return (f'{self.product.name}: {self.value} {self.currency} :'
                f'{self.description[:100]}')


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(_('user_id'), db_index=True)
    cart = models.ManyToManyField('ProductWithPrice', related_name='payments',
                                  verbose_name=_('cart'))
    payment_system = models.CharField(_('payment system'), max_length=20,
                                      db_index=True)
    payment_status = models.CharField(_('payment status'), max_length=50)
    paid = models.BooleanField(_('paid'))
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
        db_table = "admin\".\"payment"

    def __str__(self):
        return f'{self.payment_system}::{self.id}'


class ProductWithPrice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, verbose_name=_('product'),
                                related_name='carts',
                                on_delete=models.PROTECT)
    price = models.ForeignKey(Price, verbose_name=_('price'),
                              related_name='carts', on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('cart')
        db_table = "admin\".\"cart"

    def __str__(self):
        return f'{self.product.name}: {self.price.value} {self.price.currency}'
