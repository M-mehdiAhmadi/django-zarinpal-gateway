from django.contrib import admin
from django_zarinpal_gateway.models import Transaction


@admin.register(Transaction)
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

    # Show amount with thousands separator
    def formatted_amount(self, obj):
        return f"{obj.amount:,}"
    formatted_amount.short_description = "Amount (Rials)"
    formatted_amount.admin_order_field = "amount"

