from http import HTTPStatus

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from billing.models import Payment
from billing.providers import BillingProvider


@method_decorator(csrf_exempt, 'dispatch')
class TransactionView(View):

    def post(self, request, provider):

        _provider = BillingProvider.get_provider(provider)
        if not _provider:
            return JsonResponse({'error': 'Forbidden URL'},
                                status=HTTPStatus.FORBIDDEN)
        payment = _provider.proccess_request(request.body)
        if not payment:
            return JsonResponse(
                {'error': 'Impossible deserialize request body'},
                status=HTTPStatus.BAD_REQUEST)
        Payment.objects.create(**payment)
        return JsonResponse({'save': payment}, status=HTTPStatus.CREATED)
