django-zarinpal
===============

A reusable Django application that provides a clean and extensible integration
with the Zarinpal payment gateway.  
It includes request and verification views, a pluggable workflow, and a
maintainable architecture suitable for production-level payment systems.

Features
--------

- Easy integration with the Zarinpal payment API
- Transaction model and status management
- Request (payment initiation) and verification views
- Hook-based design for overriding and customization
- Gateway client wrapper (request + verify)
- Ready-to-override templates
- Fully reusable Django app structure

Quick Start
-----------

1. Install the package::

       git clone https://github.com/M-mehdiAhmadi/django-zarinpal-gateway.git

2. Add the app to your ``INSTALLED_APPS``::

       INSTALLED_APPS = [
           ...,
           "django_zarinpal_gateway",
       ]

3. Apply migrations::

       python manage.py migrate

4. Include URLs if needed::

       path("payments/", include("django_zarinpal.urls")),

5. Configure required settings in ``settings.py``::

       ZARINPAL_MERCHANT_ID = "<your-merchant-id>"

       # API endpoints
       ZA_API_REQUEST_URL = "https://payment.zarinpal.com/pg/v4/payment/request.json"
       ZA_API_VERIFY_URL  = "https://payment.zarinpal.com/pg/v4/payment/verify.json"
       ZA_API_STARTPAY_URL = "https://payment.zarinpal.com/pg/StartPay/"

Usage
-----

The app provides two core base views:

**BaseTransactionRequestView**  
Handles form submission, transaction creation, gateway request sending,
interpreting success responses, and redirecting users to the payment page.

**BaseTransactionVerifyView**  
Handles verification after the callback from Zarinpal, updates the transaction
state, and renders success or failure templates.

Both classes include customizable hooks you may override:

- ``create_gateway_client``
- ``is_request_successful`` / ``is_verified``
- ``extract_authority`` / ``get_ref_id``
- ``on_verify_success`` / ``on_verify_failed``


Settings
--------

Required:

- ``ZARINPAL_MERCHANT_ID``  
- ``ZA_API_REQUEST_URL``  
- ``ZA_API_VERIFY_URL``  
- ``ZA_API_STARTPAY_URL``  

These URLs may be replaced with sandbox or custom endpoints.

Development
-----------

Build the package locally::

    python -m build

Install the built package::

    pip install ./dist/django-zarinpal-*.tar.gz

License
-------
 
See the ``LICENSE`` file included in the package.