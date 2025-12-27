import jdatetime
from django.db import models
from django.utils.translation import gettext_lazy as _


class TransactionStatus(models.IntegerChoices):
    PENDING = 0, _("Pending")
    PAID = 1, _("Paid")
    FAILED = 2, _("Failed")


class AbstractTransaction(models.Model):

    amount = models.PositiveBigIntegerField(_("Amount"))
    authority = models.CharField(_("Authority"), max_length=64, null=True, blank=True, db_index=True)
    description = models.TextField(verbose_name=_("description"))
    mobile = models.CharField(verbose_name=_("mobile phone"),max_length=15,blank=True)
    email = models.EmailField(verbose_name=_("Email"),blank=True)
    ref_id = models.CharField(_("Reference ID"), max_length=255, null=True, blank=True, db_index=True)
    status = models.PositiveSmallIntegerField(
        _("Status"), choices=TransactionStatus.choices, default=TransactionStatus.PENDING
    )
    created_at = models.DateTimeField(_("request time"),auto_now_add=True)
    verified_at = models.DateTimeField(_("Verified At"), null=True, blank=True)

    
    class Meta:
        abstract = True
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        ordering = ["-created_at"]

    

class Transaction(AbstractTransaction):
    
    def __str__(self) -> str:
        return f"{self.pk}"

    def to_jalali(self, dt):
        return jdatetime.datetime.fromgregorian(datetime=dt) if dt else None

    @property
    def created_at_jalali(self):
        return self.to_jalali(self.created_at)
    
    def get_created_at_jalali_display(self):
        return self.created_at_jalali.strftime("%Y/%m/%d %H:%M:%S") if self.created_at_jalali else "-"

    @property
    def verified_at_jalali(self):
        return self.to_jalali(self.verified_at)
    
    def get_verified_at_jalali_display(self):
        return self.verified_at_jalali.strftime("%Y/%m/%d %H:%M:%S") if self.verified_at_jalali else "-"

    def get_status_display(self):
        """Return the human-readable label for the status choice.

        Uses the TransactionStatus enum to avoid attribute errors when
        `self.status` is an integer.
        """
        try:
            return TransactionStatus(self.status).label
        except Exception:
            return str(self.status)
    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        ordering = ["-created_at"]