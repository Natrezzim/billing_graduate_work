import datetime as dt

import pytz
from config import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import Payment


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
    def conditions_map(self):
        conditions_map = {
            'today': self.today,
            'this month': self.this_month,
            'this year': self.this_year
        }
        return conditions_map

    def lookups(self, request, model_admin):

        queryset = model_admin.get_queryset(request)

        for name, condition in self.conditions_map.items():
            if queryset.filter(**{self.field_gte: condition}).exists():
                yield (name, _(name))

    def queryset(self, request, queryset):
        if value := self.value():
            condition = self.conditions_map[value]
            return queryset.filter(**{self.field_gte: condition})


class CreatedListFilter(DateListFilter):
    title = 'date'
    parameter_name = 'created_at'
    field = 'created_at'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment_system', 'cart_id', 'date')
    list_filter = ('payment_system', CreatedListFilter)
    search_fields = ('id', 'payment_system', 'cart_id', 'date')
    ordering = ('created_at',)
    readonly_fields = ('id', 'created_at')
    fields = (('id', 'created_at'),
              'cart_id',
              ('payment_system', 'idempotence_uuid'),)

    def date(self, obj):
        return obj.created_at.date()
