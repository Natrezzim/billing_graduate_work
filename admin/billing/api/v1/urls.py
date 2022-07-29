from django.urls import path, re_path

from billing.api.v1 import views


urlpatterns = [
    path('payments/', views.TransactionView.as_view()),
    path('version/', views.VersionView.as_view()),
    path('prices/', views.ListPriceView.as_view()),
]
