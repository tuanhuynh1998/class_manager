from .models import Voucher
from student_manager.stores.models import Order
from student_manager.stores.selectors import get_order_list
from django.db.models import Q
from student_manager.users.models import User

def voucher_available_to_user(user: User) -> Voucher:
    orders = get_order_list().filter(
        Q(user=user),
        Q(status=Order.OrderStatus.COMPLETED)
        | Q(payment_status=Order.PaymentStatus.PAID)
    )
    return orders
