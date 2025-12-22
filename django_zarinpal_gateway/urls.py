from django.urls import path
from django_zarinpal_gateway import views

app_name = "zarinpal"

urlpatterns = [
    path("payment-request/", views.BaseTransactionRequestView.as_view(), name="payment_request"),
    path("payment-verify/", views.BaseTransactionVerifyView.as_view(), name="payment_verify"),
]

