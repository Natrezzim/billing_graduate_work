from django.urls import path

from billing.api.v1 import views


urlpatterns = [
    path('transactions/<str:provider>/', views.TransactionView.as_view()),
]
