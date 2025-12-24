
# django_zarinpal

A reusable Django application that provides a clean integration with the Zarinpal payment gateway.  
This package offers utilities for sending payment requests, verifying transactions, and redirecting users to the Zarinpal payment page.

## Features

- Simple API for creating and verifying Zarinpal payments  
- Fully compatible with Django projects  
- Configurable endpoints for Zarinpal sandbox or production  
- Reusable app structure following Django best practices  



## Installation
### get app with clone
```bash
git clone https://github.com/M-mehdiAhmadi/django-zarinpal-gateway.git
```
### get app with pip
```bash
pip install git+https://github.com/M-mehdiAhmadi/django-zarinpal-gateway.git
```


### Add the app to your Django project :
#### if you want to use defulte app
```python
INSTALLED_APPS = [
    ...
    "django_zarinpal_gateway",
]
```
#### if you want to use custom app
```python
INSTALLED_APPS = [
    ...
    "your_custom_app",
]
```
---

## Configuration

Add the following settings to `settings.py`:

```python
ZARINPAL_MERCHANT_ID = "YOUR_MERCHANT_ID"

ZARINPAL_API_REQUEST_URL = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZARINPAL_API_VERIFY_URL = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZARINPAL_API_STARTPAY_URL = "https://www.zarinpal.com/pg/StartPay/"

ZARINPAL_CALLBACK_URL = "your_callback_url"
```

---

## Usage

### Creating a payment request

```python
from django_zarinpal_gateway.views import BaseTransactionRequestView

class MyPaymentRequestView(BaseTransactionRequestView):
    template_name = "myapp/custom_payment_form.html"

```

### Verifying the payment

```python
from django_zarinpal_gateway.views import BaseTransactionVerifyView
from django.shortcuts import render

class MyPaymentVerifyView(BaseTransactionVerifyView):
    def on_verify_success(self, transaction: Transaction, ref_id: str):
        # your logic on success
        return render(self.request, "myapp/payment-success.html", {"transaction": transaction})

    def on_verify_failed(self, transaction: Transaction, result: dict):
        # your logic on failed
        return render(self.request, "myapp/payment-failed.html", {"transaction": transaction, "result": result})

```

---

## Contributing

Pull requests are welcome.
Follow Django’s reusable app structure as recommended in the official documentation.

---
