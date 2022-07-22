from http import HTTPStatus

import orjson
from billing.models import Payment
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, 'dispatch')
class TransactionView(View):

    def post(self, request):
        if not request.body:
            return JsonResponse({'error': 'Empty request body'},
                                status=HTTPStatus.BAD_REQUEST)
        body = orjson.loads(request.body)
        items = body.get('items')
        if not items:
            return JsonResponse({'error': 'Incorrect JSON scheme'},
                                status=HTTPStatus.BAD_REQUEST)
        try:
            Payment.objects.bulk_create(
                [Payment(**payment) for payment in items]
            )
        except IntegrityError:
            return JsonResponse({'error': 'DB Integrity Error'},
                                status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({'status': 'success'}, status=HTTPStatus.CREATED)
