from django.db import models
from student_manager.stores.models import Order

class Promo(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True, unique=True)
    description = models.CharField(max_length=255, default="")
    self_order_only = models.BooleanField(default=False)
    discount_amount = models.IntegerField()
    minimum_order_amount = models.IntegerField()
    min_order_count = models.IntegerField(default=0)
    max_order_count = models.IntegerField(default=0)
    max_claims = models.IntegerField(default=0)
    expires_at = models.DateTimeField(null=True, blank=True, db_index=True)
    active = models.BooleanField(default=True)
    special = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class UserPromoClaim(models.Model):
    promo = models.ForeignKey(Promo, related_name="user_claims", on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order,
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
