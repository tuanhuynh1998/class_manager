from commons.exceptions import ValidationException
from .models import Voucher
from datetime import datetime, timedelta

def create_voucher(*,
    name: str,
    code: str,
    user_limit: int,
    max_redemption: int,
    promo_type: str,
    discount_value: int,
    minimum_order_amount: int,
    min_order_count: int,
    max_order_count: int,
    exclusive_to_user: bool,
    active: bool,
    claimable: bool
) -> Voucher:
    voucher_check = Voucher.objects.filter(name=name, code=code).exists()
    if voucher_check:
        raise ValidationException({"message": "unique error"})
    voucher = Voucher.objects.create(
        name=name,
        code=code,
        user_limit=user_limit,
        max_redemption=max_redemption,
        valid_until=datetime.now()+timedelta(days=30),
        promo_type=promo_type,
        discount_value=discount_value,
        minimum_order_amount=minimum_order_amount,
        min_order_count=min_order_count,
        max_order_count=max_order_count,
        exclusive_to_user=exclusive_to_user,
        active=active,
        claimable=claimable
    )

    return voucher
