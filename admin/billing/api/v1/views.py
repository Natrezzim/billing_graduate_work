import logging
from http import HTTPStatus

import orjson
import structlog
from billing.models import Payment, Price, ProductWithPrice
from billing.validators import ValidListPayments, ValidPrice, ValidProduct
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from pydantic import ValidationError


@method_decorator(csrf_exempt, 'dispatch')
class TransactionView(View):

    update_fields = ['payment_status', 'paid', 'updated_at']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.logger = structlog.get_logger(self.__class__.__name__)

    def _separate_records(self, records):
        records_for_update = []
        records_for_create = []
        payments_ids = Payment.objects.values_list('id', flat=True)

        for record in records:
            if record.id in payments_ids:
                records_for_update.append(record)
            else:
                records_for_create.append(record)

        return records_for_update, records_for_create

    def _bulk_update(self, records):
        updates = []
        for record in records:
            record = record.dict()
            _ = record.pop('cart')
            payment = Payment(**record)
            updates.append(payment)

        Payment.objects.bulk_update(updates, self.update_fields)

    def _create(self, records):
        for record in records:
            record = record.dict()
            cart_data = record.pop('cart')
            payment = Payment.objects.create(**record)
            for product in cart_data:
                pwp_obj, _ = ProductWithPrice.objects.get_or_create(**product)
                payment.cart.add(pwp_obj)

    def post(self, request):
        if not request.body:
            return JsonResponse({'error': 'Empty request body'},
                                status=HTTPStatus.BAD_REQUEST)
        body = orjson.loads(request.body)
        try:
            records = ValidListPayments(**body).items
        except ValidationError:
            return JsonResponse({'error': 'Incorrect JSON schema'},
                                status=HTTPStatus.BAD_REQUEST)

        records_for_update, records_for_create = self._separate_records(records)

        try:
            self._create(records_for_create)
            self._bulk_update(records_for_update)
        except IntegrityError:
            return JsonResponse({'error': 'Incorrect data in request'},
                                status=HTTPStatus.BAD_REQUEST)

        result = {
            'status': 'success',
            'details': {
                'updated': len(records_for_update),
                'created': len(records_for_create)
            }
        }

        return JsonResponse(result, status=HTTPStatus.CREATED)


class ListPriceView(View):

    required_fields = [
            'product__id', 'product__name', 'product__type',
            'product__description', 'id', 'value', 'currency',
            'description', 'is_active'
        ]
    product_keys = ['id', 'name', 'type', 'description']
    price_keys = ['id', 'value', 'currency', 'description', 'is_active']

    def _transform_to_products(self, values):

        products = []
        current = None
        if values:
            for record in values:
                product = ValidProduct(**dict(zip(self.product_keys, record[:4])))
                price = ValidPrice(**dict(zip(self.price_keys, record[4:])))
                current = current if current else product
                if product.id != current.id:
                    products.append(current.dict())
                    current = product
                current.prices.append(price)

            products.append(current.dict())

        return products

    def get(self, request):
        queryset = Price.objects.filter(is_active=True).order_by('product__id')
        values = queryset.values_list(*self.required_fields)

        products = self._transform_to_products(values)

        result = {
            'total': len(products),
            'items': products
        }
        return JsonResponse(result, status=HTTPStatus.OK)


class VersionView(View):

    version = 'v1.290722'

    def get(self, request):
        return JsonResponse({'version': self.version}, status=HTTPStatus.OK)


class StubView(View):

    version = 'v1.290722'

    def get(self, request):
        return JsonResponse({'error': 'Page not found'},
                            status=HTTPStatus.NOT_FOUND)
