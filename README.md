
# django_zarinpal_gateway

A reusable Django app that provides a simple integration with the Zarinpal payment gateway. This package includes utilities for creating payment requests, verifying transactions, and redirecting users to Zarinpal's payment page.

## Table of Contents
- [django\_zarinpal\_gateway](#django_zarinpal_gateway)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Clone the repository](#clone-the-repository)
    - [Install via pip](#install-via-pip)
    - [Add the app to your Django project](#add-the-app-to-your-django-project)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [Create a payment app](#create-a-payment-app)
      - [Views](#views)
      - [URLs](#urls)
      - [Models](#models)
  - [Contributing](#contributing)

## Installation

### Clone the repository
```bash
git clone https://github.com/M-mehdiAhmadi/django-zarinpal-gateway.git
```

### Install via pip
```bash
pip install git+https://github.com/M-mehdiAhmadi/django-zarinpal-gateway.git
```

### Add the app to your Django project
Add `django_zarinpal_gateway` to `INSTALLED_APPS` in your `settings.py`:

```python
INSTALLED_APPS = [
    ...
    "django_zarinpal_gateway",
]
```

## Configuration

Add the following settings to `settings.py`:

```python
ZARINPAL_MERCHANT_ID = "YOUR_MERCHANT_ID"

ZARINPAL_API_REQUEST_URL = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZARINPAL_API_VERIFY_URL = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZARINPAL_API_STARTPAY_URL = "https://www.zarinpal.com/pg/StartPay/"

ZARINPAL_CALLBACK_URL = "https://your-domain.com/payment-verify/"
```

## Usage

### Create a payment app

#### Views
To create a payment request view, inherit from `BaseTransactionRequestView` and set `template_name`:

```python
from django_zarinpal_gateway.views import BaseTransactionRequestView

class MyPaymentRequestView(BaseTransactionRequestView):
    template_name = "payment/custom-payment-form.html"
```

To show a custom error page when a request to Zarinpal fails, set or override `error_template`:

```python
error_template = "payment/your-transaction-error.html"
```

To verify payments, inherit from `BaseTransactionVerifyView` and set `success_template` and `failed_template`:

```python
from django_zarinpal_gateway.views import BaseTransactionVerifyView

class MyPaymentVerifyView(BaseTransactionVerifyView):
    success_template = "payment/verify-success.html"
    failed_template = "payment/verify-failed.html"
```

When a payment is successful, the `on_verify_success` method is called. When verification fails, `on_verify_failed` is called. Override these methods to add your custom logic:

```python
from django.contrib.auth.mixins import LoginRequiredMixin

class MyPaymentVerifyView(LoginRequiredMixin, BaseTransactionVerifyView):
    success_template = "payment/verify-success.html"
    failed_template = "payment/verify-failed.html"

    def on_verify_success(self, transaction: Transaction, ref_id: str):
        """Handle successful verification."""
        # your logic here
        super().on_verify_success(transaction, ref_id)

    def on_verify_failed(self, transaction: Transaction, result):
        """Handle failed verification."""
        # your logic here
        super().on_verify_failed(transaction, result)
```

#### URLs
Add a URL for creating the payment request (use `MyPaymentRequestView`) and one for verification (use `MyPaymentVerifyView`). Note: Zarinpal sends `authority` as a query parameter in the callback.

Example `urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("payment-request/", views.MyPaymentRequestView.as_view(), name="payment_request"),
    path("payment-verify/<str:authority>/", views.MyPaymentVerifyView.as_view(), name="payment_verify"),
    path("payment-verify/", views.MyPaymentVerifyView.as_view(), name="payment_verify_queryset"),
]
```

The `MyPaymentVerifyView` can accept `authority` as a path parameter and may also receive callback data via query parameters.

#### Models
The package provides an `AbstractTransaction` model you can extend for storing payments. A ready `Transaction` model is included in the app; you may subclass `AbstractTransaction` to add custom fields.

Key fields (from `AbstractTransaction`):
- `amount` — the payment amount (integer).
- `authority` — Zarinpal authority token (indexed, may be null until request).
- `description` — optional text describing the transaction.
- `mobile` — optional payer mobile phone.
- `email` — optional payer email.
- `ref_id` — reference ID returned by Zarinpal after verification (indexed).
- `status` — integer choice: Pending / Paid / Failed (see `TransactionStatus`).
- `created_at` — request timestamp.
- `verified_at` — verification timestamp (nullable).

Helper properties and methods available on the `Transaction` model:
- `to_jalali(dt)` — convert a Gregorian `datetime` to Jalali (uses `jdatetime`).
- `created_at_jalali` / `verified_at_jalali` — Jalali datetime properties.
- `get_created_at_jalali_display()` / `get_verified_at_jalali_display()` — formatted Jalali datetime strings (safe for null values).
- `get_status_display()` — returns the human-readable status label.

Example: extend `AbstractTransaction` to add fields or behavior:

```python
from django.db import models
from django_zarinpal_gateway.models import AbstractTransaction

class Transaction(AbstractTransaction):
    # add your custom fields here
    extra_info = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return str(self.pk)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-created_at"]
```

## Contributing

Pull requests are welcome. Please follow Django’s recommended structure for reusable apps as described in the official documentation.

---
