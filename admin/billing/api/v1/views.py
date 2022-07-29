import logging
from http import HTTPStatus

import orjson
import structlog
from billing.models import Payment, Product, ProductWithPrice, Price
from billing.validators import ValidListPayments, ValidPrice, ValidProduct
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from pydantic import ValidationError


@method_decorator(csrf_exempt, 'dispatch')
class TransactionView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.logger = structlog.get_logger(self.__class__.__name__)

    def post(self, request):
        if not request.body:
            return JsonResponse({'error': 'Empty request body'},
                                status=HTTPStatus.BAD_REQUEST)
        body = orjson.loads(request.body)
        try:
            records = ValidListPayments(**body).items
        except ValidationError:
            return JsonResponse({'error': 'Incorrect JSON scheme'},
                                status=HTTPStatus.BAD_REQUEST)

        for record in records:
            record = record.dict()
            cart_data = record.pop('cart')
            payment, _ = Payment.objects.get_or_create(**record)
            payment.cart.clear()
            for product in cart_data:
                obj, _ = Product.objects.get_or_create(**product)
                payment.cart.add(obj)

        return JsonResponse({'status': 'success'}, status=HTTPStatus.CREATED)


class ListPriceView(View):

    required_fields = [
            'product__id', 'product__name', 'product__type',
            'product__description', 'id', 'value', 'currency',
            'description', 'is_active'
        ]
    product_key = ['id', 'name', 'type', 'description']
    price_key = ['id', 'value', 'currency', 'description', 'is_active']

    def get(self, request):
        base_qs = Price.objects.filter(is_active=True).order_by('product__id')
        queryset = base_qs.values_list(*self.required_fields)
        products = []
        current = None
        for record in queryset:
            product = ValidProduct(**dict(zip(self.product_key, record[:4])))
            price = ValidPrice(**dict(zip(self.price_key, record[4:])))
            current = current if current else product
            if product.id != current.id:
                products.append(current.dict())
                current = product
            current.prices.append(price)

        products.append(current.dict())

        c = sum(1 for product in products for price in product['prices'])
        print(c)

        return JsonResponse(products, safe=False, status=HTTPStatus.OK)


class VersionView(View):

    version = 'v1.290722'

    def get(self, request):
        return JsonResponse({'version': self.version}, status=HTTPStatus.OK)


class StubView(View):

    version = 'v1.290722'

    def get(self, request):
        return JsonResponse({'error': 'Page not found'},
                            status=HTTPStatus.NOT_FOUND)
