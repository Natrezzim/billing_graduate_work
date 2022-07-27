import logging
from http import HTTPStatus

import orjson
import structlog
from billing.models import Payment, Product
from billing.validators import ValidListPayments
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from pydantic import ValidationError


@method_decorator(csrf_exempt, 'dispatch')
class TransactionView(View):

    def __init__(self, *args, **kwargs):
        self.logger = structlog.get_logger(self.__class__.__name__)
        super().__init__(self, *args, **kwargs)

    version = 'v1.230722'

    def get(self, request):
        return JsonResponse({'version': self.version}, status=HTTPStatus.OK)

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
