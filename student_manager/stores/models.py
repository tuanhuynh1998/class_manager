from django.db import models
from django.utils import timezone
from student_manager.users.models import User
from commons.exceptions import ValidationException
from django.utils.translation import gettext_lazy as _

def store_img_path(instance, filename):
    return f"stores/{instance.url}/{filename}"

class DeliveryAddress(models.Model):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    mobile_number = models.CharField(max_length=255, blank=True, db_index=True)
    address = models.CharField(max_length=255, default="", blank=True)
    city = models.CharField(max_length=255, default="", blank=True)
    province = models.CharField(max_length=255, default="", blank=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)

class StoreAddress(models.Model):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    mobile_number = models.CharField(max_length=255, blank=True, db_index=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    province = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)

class Store(models.Model):
    user = models.ForeignKey(
        "users.User", related_name="stores", on_delete=models.PROTECT
    )
    image = models.ImageField(upload_to=store_img_path, null=True, blank=True)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    landmark = models.TextField()
    latitude = models.DecimalField(
        max_digits=11, decimal_places=8, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=11, decimal_places=8, null=True, blank=True
    )
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    created_at = models.DateTimeField(auto_now=timezone.now())

    def __str__(self):
        return self.url

class Cart(models.Model):
    owner = models.ForeignKey(
        "users.User",
        related_name="carts",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    ordering_for = models.ForeignKey(
        "users.User",
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    store = models.ForeignKey(
        Store, related_name="carts", on_delete=models.CASCADE, null=True
    )
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    created_at = models.DateTimeField(auto_now=timezone.now())

    def save(self, *args, **kwargs) -> None:
        if self.ordering_for:
            try:
                User.objects.get(pk=self.ordering_for.id)
            except:
                raise ValidationException({"message": "validation error"})
        super().save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(default="", blank=True)
    average_cost = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    status = models.CharField(max_length=20, null=True, db_index=True, blank=True)
    sellable = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    created_at = models.DateTimeField(auto_now=timezone.now())

    class Meta:
        unique_together = ('name', 'brand',)

class Order(models.Model):
    class DeliveryMethod(models.TextChoices):
        DELIVERY = "DELIVERY", "Deliver"
        PICKUP = "PICKUP", "Pickup"

    class OrderStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        FOR_APPROVAL = "FOR_APPROVAL", "For approval"
        FOR_PROCESSING = "FOR_PROCESSING", "For processing"
        PROCESSING = "PROCESSING", "Processing"
        FOR_DISPATCH = "FOR_DISPATCH", "For Dispatch"
        DISPATCHED = "DISPATCHED", "Dispatched"
        ENROUTE = "ENROUTE", "Enroute"
        ARRIVED = "ARRIVED", "Arrived"
        RECEIVED = "RECEIVED", "Received"
        TO_PACK = "TO_PACK", "To Pack"
        CANCELED = "CANCELED", "Canceled"
        REJECTED = "REJECTED", "Rejected"
        COMPLETED = "COMPLETED", "Completed"
        DELIVERY_FAILED = "DELIVERY_FAILED", "Delivery Failed"
        RETURNED = "RETURNED", "Returned"

    class PaymentStatus(models.TextChoices):
        TO_COLLECT = "TO_COLLECT", "To collect"
        UNPAID = "UNPAID", "Unpaid"
        PAID = "PAID", "Paid"

    order_number = models.CharField(
        max_length=32, db_index=True
    )
    store = models.ForeignKey(
        Store, related_name="orders", on_delete=models.SET_NULL, null=True, blank=True
    )
    user = models.ForeignKey(
        "users.User",
        related_name="orders",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    cart = models.ForeignKey(
        Cart, related_name="orders", on_delete=models.SET_NULL, null=True, blank=True
    )
    delivery_method = models.CharField(
        max_length=32,
        choices=DeliveryMethod.choices,
        null=True,
        blank=True,
        db_index=True,
    )
    store_address = models.ForeignKey(
        StoreAddress, related_name="+", on_delete=models.SET_NULL, null=True
    )
    delivery_address = models.ForeignKey(
        DeliveryAddress, related_name="+", on_delete=models.SET_NULL, null=True
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.TO_COLLECT,
        db_index=True,
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        db_index=True,
    )
    total_discount_amount = models.IntegerField(default=0)
    total_items_amount = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)
    
    estimated_delivery_date = models.DateField(null=True, blank=True, db_index=True)
    approved_at = models.DateTimeField(null=True, blank=True, db_index=True)
    canceled_at = models.DateTimeField(null=True, blank=True, db_index=True)
    received_at = models.DateTimeField(null=True, blank=True, db_index=True)
    
    updated_at = models.DateTimeField(auto_now_add=timezone.now())
    created_at = models.DateTimeField(auto_now=timezone.now())

class StoreProductConfig(models.Model):
    store = models.ForeignKey(
        Store, related_name="product_configs", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="store_configs", on_delete=models.CASCADE
    )
    price_adjustment = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    sellable = models.BooleanField(default=True)

    class Meta:
        unique_together = ("store", "product")

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="line_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)

    class Meta:
        ordering = ["id"]

    @property
    def subtotal(self):
        return self.product.total_price * self.quantity

class ProcessingCutoff(models.Model):
    class OrderDays(models.IntegerChoices):
        MONDAY = 1, _("Monday")
        TUESDAY = 2, _("Tuesday")
        WEDNESDAY = 3, _("Wednesday")
        THURSDAY = 4, _("Thursday")
        FRIDAY = 5, _("Friday")
        SATURDAY = 6, _("Saturday")
        SUNDAY = 7, _("Sunday")

    class DeliveryDays(models.IntegerChoices):
        TODAY = 0, _("On the Order Day")
        MONDAY = 1, _("Next Monday")
        TUESDAY = 2, _("Next Tuesday")
        WEDNESDAY = 3, _("Next Wednesday")
        THURSDAY = 4, _("Next Thursday")
        FRIDAY = 5, _("Next Friday")
        SATURDAY = 6, _("Next Saturday")
        SUNDAY = 7, _("Next Sunday")

    order_day = models.IntegerField(
        _("Order Day"), default=0, choices=OrderDays.choices
    )
    start_time = models.TimeField(_("From Order Time"), default="00:00:00")
    end_time = models.TimeField(_("To Order Time"), default="23:59:59")
    cutoff_day = models.IntegerField(
        _("Cutoff Day"), default=0, choices=DeliveryDays.choices
    )
    cutoff_time = models.TimeField(_("Cutoff Day"), default="17:00:00")
    delivery_day = models.IntegerField(
        _("Delivery Day"), default=0, choices=DeliveryDays.choices
    )

class OrderPromo(models.Model):
    order = models.ForeignKey(Order, related_name="promos", on_delete=models.CASCADE)
    # promo = models.ForeignKey(
    #     "promo.Promo",
    #     related_name="+",
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    # )
    code = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255)
    discount_amount = models.IntegerField()
