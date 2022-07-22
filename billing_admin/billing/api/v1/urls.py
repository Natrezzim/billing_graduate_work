from django.urls import path

from billing.api.v1 import views


urlpatterns = [
    path('payments/', views.TransactionView.as_view()),
]
