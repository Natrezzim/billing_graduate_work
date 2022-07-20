from http import HTTPStatus

import orjson
from billing.models import Payment
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, 'dispatch')
class TransactionView(View):

    def post(self, request):

        body = orjson.loads(request.body)
        items = body.get('items')
        if not items:
            return JsonResponse({'error': 'Empty request'},
                                status=HTTPStatus.BAD_REQUEST)
        for payment in items:
            Payment.objects.create(**payment)

        return JsonResponse({'status': 'success'}, status=HTTPStatus.CREATED)
