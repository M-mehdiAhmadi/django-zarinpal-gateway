from django.urls import path
from . import views

app_name = "zarinpal"

urlpatterns = [
    path("payment-request/<int:pk>/", views.PaymentRequestView.as_view(), name="payment_request"),
    path("payment-verify/", views.PaymentVerifyView.as_view(), name="payment_verify"),
]

