import datetime as dt

import pytz
from config import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from billing.models import Payment, Price, Product, ProductWithPrice

admin.site.unregister(Group)


class DateListFilter(admin.SimpleListFilter):
    '''
    Класс для фильтрации по полям DateField
    '''

    field = str()
    timezone = pytz.timezone(settings.TIME_ZONE)

    @property
    def today(self):
        return dt.datetime.now(self.timezone).date()

    @property
    def this_year(self):
        return dt.datetime(self.today.year, 1, 1, tzinfo=self.timezone)

    @property
    def this_month(self):
        return dt.datetime(
            self.today.year, self.today.month, 1, tzinfo=self.timezone
        )

    @property
    def field_gte(self):
        return self.field + '__gte'

    @property
    def field_lt(self):
        return self.field + '__lt'

    @property
    def conditions_map(self):
        conditions_map = {
            'today': (self.today, self.field_gte),
            'this month': (self.this_month, self.field_gte),
            'this year': (self.this_year, self.field_gte),
            'previous years': (self.this_year, self.field_lt),
        }
        return conditions_map

    def lookups(self, request, model_admin):

        queryset = model_admin.get_queryset(request)

        for name, condition in self.conditions_map.items():
            value, field_condition = condition
            if queryset.filter(**{field_condition: value}).exists():
                yield (name, _(name))

    def queryset(self, request, queryset):
        if value := self.value():
            condition = self.conditions_map[value]
            value, field_condition = condition
            return queryset.filter(**{field_condition: value})


class CreatedListFilter(DateListFilter):
    title = 'date'
    parameter_name = 'created_at'
    field = 'created_at'


class ProductInline(admin.TabularInline):
    model = ProductWithPrice.payments.through
    verbose_name = 'Product'
    verbose_name_plural = 'Cart of Products'
    raw_id_fields = ('payment',)
    extra = 0
    min_num = 1


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'user_id', 'payment_system', 'date', 'paid', 'payment_status',
    )
    list_filter = ('payment_system', CreatedListFilter, 'paid', 'payment_status',)
    search_fields = (
        'id', 'user_id', 'payment_system', 'paid', 'cart__name',
    )
    ordering = ('created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fields = (('id', 'created_at', 'updated_at'),
              'user_id',
              ('payment_system', 'payment_status', 'paid'),)
    inlines = [ProductInline]

    def date(self, obj):
        return obj.created_at.date()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'type', 'description')
    ordering = ('name',)
    readonly_fields = ('id', 'created_at', 'updated_at',)
    list_filter = ('name', 'type')
    search_fields = ('name', 'type')
    fields = (('id', 'created_at', 'updated_at'),
              ('name', 'type', 'description'))


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):

    list_display = ('id', 'product', 'value', 'currency', 'is_active',
                    'description', 'count_active_price')
    ordering = ('-is_active', 'product__name', 'currency',)
    readonly_fields = ('id', 'created_at', 'updated_at',)
    list_filter = ('is_active', 'currency', 'product')
    search_fields = ('product__name', 'currency', 'description')
    fields = (('id', 'created_at', 'updated_at'),
              'is_active',
              ('product', 'value', 'currency', 'description'))

    def count_active_price(self, obj):
        return Price.objects.filter(product__id=obj.product.id, is_active=True,
                                    currency=obj.currency).count()


@admin.register(ProductWithPrice)
class ProductWithPriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'price',)
    ordering = ('id',)
    readonly_fields = ('id', 'created_at', 'updated_at',)
    fields = (('id', 'created_at', 'updated_at'),
              ('product', 'price'))