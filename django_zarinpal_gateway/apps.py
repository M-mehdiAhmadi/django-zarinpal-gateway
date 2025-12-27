from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class MultipayConfig(AppConfig):
    name = "django_zarinpal_gateway"
    verbose_name = _("payment (zarinpal)")