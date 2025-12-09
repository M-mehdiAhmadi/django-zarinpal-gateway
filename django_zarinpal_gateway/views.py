from django.conf import settings
from django.shortcuts import redirect, render
from django.views.generic import CreateView,DetailView
from .models import Transaction, TransactionStatus
from .zarinpal import Zarinpal
from . import forms


class BaseTransactionRequestView(CreateView):
    """
    Base view for initiating a Zarinpal payment transaction.

    This view handles:
    - Creating a Transaction instance using the provided form.
    - Initializing the gateway client (Zarinpal).
    - Sending the payment request to the provider.
    - Validating the provider response.
    - Storing the returned authority code.
    - Redirecting the user to the Zarinpal payment page on success.
    - Rendering an error page on failure.

    Override hooks for customization:
    - get_initial_status()         → Define initial transaction status.
    - create_gateway_client()      → Customize gateway client creation.
    - send_request()               → Customize API call logic.
    - is_request_successful()      → Define success condition.
    - extract_authority()          → Extract authority token from response.
    - get_redirect_url()           → Customize final redirect URL.
    - handle_request_error()       → Define provider-error behavior.

    Expected behavior:
    - form_valid() orchestrates the full lifecycle of creating the
      transaction, calling the provider, and redirecting the user.
    """
    form_class = forms.TransactionForm
    queryset = Transaction.objects.all()

    # -----------------------------
    # Hooks for customization
    # -----------------------------
    def get_initial_status(self):
        """Initial status when transaction is created."""
        return TransactionStatus.PENDING

    def create_gateway_client(self, transaction: Transaction):
        """Return Zarinpal client instance."""
        return Zarinpal(
            request=self.request,
            amount=transaction.amount,
            description=transaction.description or "",
            mobile=transaction.mobile or "",
            email=transaction.email or "",
        )

    def send_request(self, client: Zarinpal):
        """Call the provider and return its raw response."""
        return client.send_request()

    def is_request_successful(self, result: dict):
        """Check if provider response is success."""
        return "data" in result and result["data"].get("code") == 100

    def extract_authority(self, result: dict):
        """Extract authority from provider response."""
        return result["data"]["authority"]

    def get_redirect_url(self, authority: str):
        """Generate redirect URL."""
        return f"{settings.ZARINPAL_STARTPAY_URL}{authority}"

    def handle_request_error(self, result: dict):
        """Render error page."""
        return render(self.request, "zarinpal/transaction-error.html", {"result": result})

    # -----------------------------
    # Orchestration
    # -----------------------------
    def form_valid(self, form):
        transaction: Transaction = form.save(commit=False)
        transaction.status = self.get_initial_status()
        transaction.save()

        # Provider client
        client = self.create_gateway_client(transaction)

        # Send request
        result = self.send_request(client)

        # Success / error
        if self.is_request_successful(result):
            authority = self.extract_authority(result)
            transaction.authority = authority
            transaction.save(update_fields=["authority"])
            return redirect(self.get_redirect_url(authority))

        return self.handle_request_error(result)



class BaseTransactionVerifyView(DetailView):
    """
    Base view for verifying a Zarinpal transaction after user returns
    from the payment gateway.

    Responsibilities:
    - Resolve the Transaction instance using the authority code.
    - Initialize the gateway client for verification.
    - Call the provider’s verify API.
    - Interpret the verification result.
    - Update transaction status and store RefID on success.
    - Render appropriate success or failure templates.

    Customizable hooks:
    - get_transaction()          → Retrieve the transaction object.
    - get_authority()            → Resolve authority from URL/query.
    - create_gateway_client()    → Customize verification client.
    - send_verify_request()      → Call provider verification API.
    - is_verified()              → Define success condition.
    - get_ref_id()               → Extract provider RefID.
    - on_verify_success()        → Handle success path.
    - on_verify_failed()         → Handle failure path.

    Flow:
    - get(): orchestrates the verification procedure, starting from
      fetching the transaction and authority, calling the gateway,
      validating the response, and delegating to success/failure handlers.
    """
    model = Transaction
    slug_field = "authority"
    slug_url_kwarg = "authority"

    # -----------------------------
    # Hooks for customization
    # -----------------------------
    def get_transaction(self):
        """Return transaction instance."""
        return self.get_object()

    def get_authority(self):
        """Read authority from query or URL."""
        return self.kwargs.get(self.slug_url_kwarg)

    def create_gateway_client(self, transaction: Transaction):
        """Provider client for verification."""
        return Zarinpal(
            request=self.request,
            amount=transaction.amount,
        )

    def send_verify_request(self, client: Zarinpal, authority: str):
        """Call provider verify API."""
        return client.verify(authority)

    def is_verified(self, result):
        """Check if provider verification succeeded."""
        return "data" in result and result["data"].get("code") == 100

    def get_ref_id(self, result):
        """Extract tracking code / RefID."""
        return result["data"]["ref_id"]

    def on_verify_success(self, transaction:Transaction, ref_id: str):
        """What to do on success."""
        transaction.status = TransactionStatus.PAID
        transaction.ref_id = ref_id
        transaction.save(update_fields=["status", "ref_id"])
        return render(self.request, "zarinpal/verify-success.html", {"transaction": transaction})

    def on_verify_failed(self, transaction, result):
        """What to do on failure."""
        transaction.status = TransactionStatus.FAILED
        transaction.save(update_fields=["status"])
        return render(self.request, "zarinpal/verify-failed.html", {"transaction": transaction, "result": result})

    # -----------------------------
    # Orchestration
    # -----------------------------
    def get(self, request, *args, **kwargs):
        self.request = request
        transaction = self.get_transaction()
        authority = self.get_authority()

        client = self.create_gateway_client(transaction)
        result = self.send_verify_request(client, authority)

        if self.is_verified(result):
            ref_id = self.get_ref_id(result)
            return self.on_verify_success(transaction, ref_id)

        return self.on_verify_failed(transaction, result)
