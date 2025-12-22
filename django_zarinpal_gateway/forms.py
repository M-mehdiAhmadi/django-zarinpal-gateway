from django import forms
from django_zarinpal_gateway.models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "amount",      # user can set
            "description", # optional
            "email",       # optional
            "mobile",      # optional
        ]
