from django import forms
from django_zarinpal_gateway.models import Transaction
from django.utils.translation import gettext_lazy as _

class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["amount"].label = _("Amount to Pay")
        self.fields["description"].label = _("Description")
        self.fields["email"].label = _("Email")
        self.fields["mobile"].label = _("Mobile")
    class Meta:
        model = Transaction
        fields = [
            "amount",      # user can set
            "description", # optional
            "email",       # optional
            "mobile",      # optional
        ]
