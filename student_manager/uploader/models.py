from django.db import models
from django.utils import timezone
from datetime import datetime

from commons.exceptions import ValidationException

class Upload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField()

    @property
    def image_url(self):
        return self.file.url

class Invoice(models.Model):
    class InvoiceStatus(models.TextChoices):
        NOT_AVAILABLE = 0, "Not Available"
        PENDING = 1, "Pending"
        DRAFT = 2, "Draft"
        AUTHORIZED = 3, "Authorised"
        PAID = 4, "Paid"
        PARTIALLY_PAID = 5, "Partially Paid"

    user = models.ForeignKey("users.User", related_name="invoices", on_delete=models.PROTECT)
    invoice_number = models.CharField(max_length=20)
    invoice_amount = models.FloatField()
    invoice_date = models.DateField(null=True, blank=True)
    invoice_due_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    created_at = models.DateTimeField(auto_now=timezone.now())
    status = models.IntegerField(choices=InvoiceStatus.choices, default=InvoiceStatus.PENDING)

    def save(self, *args, **kwargs):
        self_date = datetime.strptime(self.invoice_date, '%Y-%m-%d')
        self_year = self_date.year
        self_month = self_date.month
        invoice = Invoice.objects.filter(
            user=self.user,
            invoice_date__year=self_year,
            invoice_date__month=self_month
        )
        if invoice:
            raise ValidationException({"message": "Duplicate invoice"})
        super().save(*args, **kwargs)

class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 0, "Pending"
        PAID = 1, "Paid"
        EXPIRED = 2, "Expired"

    invoice = models.ForeignKey(Invoice, related_name="payments", on_delete=models.CASCADE)
    status = models.IntegerField(choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)
