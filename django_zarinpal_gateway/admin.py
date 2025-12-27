from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_zarinpal_gateway import models

class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "formatted_amount",
        "get_status_display",
        "get_created_at_jalali_display",
        "get_verified_at_jalali_display",
    )
    list_filter = ("status", "created_at", "verified_at")
    search_fields = ("authority", "ref_id")
    readonly_fields = (
        "get_created_at_jalali_display",
        "get_verified_at_jalali_display",
        "get_status_display",
    )
    list_per_page = 100
    
    @admin.display(description=_("created at"))
    def get_created_at_jalali_display(self, obj:models.Transaction):
        return obj.get_created_at_jalali_display()

    @admin.display(description=_("Verified At"))
    def get_verified_at_jalali_display(self, obj:models.Transaction):
        return obj.get_verified_at_jalali_display()

    @admin.display(description=_("status"))
    def get_status_display(self, obj:models.Transaction):
        return obj.get_status_display()
    
    # Show amount with thousands separator
    def formatted_amount(self, obj):
        return f"{obj.amount:,}"
    formatted_amount.short_description = _("Amount (Rials)")
    formatted_amount.admin_order_field = "amount"

