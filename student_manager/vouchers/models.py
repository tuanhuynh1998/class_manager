from django.db import models
from student_manager.users.models import User
from student_manager.stores.models import Order, Cart

class Voucher(models.Model):
    class UserType(models.TextChoices):
        ANY = "ANY", "Anyone"
        CL = "CL", "Community Leader"
        SUKI = "SUKI", "Suki"

    class VoucherType(models.TextChoices):
        CART_FIXED = "CART_FIXED", "Fixed Amount Discount Applied to Cart Total"
        CART_PERCENTAGE = "CART_PERCENTAGE", "Percentage Discount Applied to Cart Total"
        PRODUCT_FIXED = (
            "PRODUCT_FIXED",
            "Fixed Amount Discount Applied to Product Total",
        )
        PRODUCT_FIXED_PER_ITEM = (
            "PRODUCT_FIXED_PER_ITEM",
            "Fixed Amount Discount Applied to Product Per Item",
        )
        PRODUCT_PERCENTAGE = (
            "PRODUCT_PERCENTAGE",
            "Percentage Discount Applied to Product Total",
        )

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    user_limit = models.PositiveIntegerField(
        default=1,
    )
    max_redemption = models.PositiveIntegerField(
        default=0,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(
        blank=True,
        null=True,
    )
    promo_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=VoucherType.choices,
    )
    promo_users = models.CharField(max_length=20, default=UserType.ANY, choices=UserType.choices)
    discount_value = models.IntegerField()
    minimum_order_amount = models.IntegerField()
    min_order_count = models.IntegerField(default=0)
    max_order_count = models.IntegerField(default=0)
    exclusive_to_user = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    claimable = models.BooleanField(default=True)

class VoucherUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    redeem_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = (("voucher", "user"),)

class VoucherRedemption(models.Model):
    voucher = models.ForeignKey(
        Voucher, related_name="redemptions", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    redeemed_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="voucher_redemptions",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="voucher_redemptions",
    )
    discount_amount = models.IntegerField()
