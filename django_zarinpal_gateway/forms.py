from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "amount",      # user can set
            "description", # optional
            "email",       # optional
            "mobile",      # optional
        ]
