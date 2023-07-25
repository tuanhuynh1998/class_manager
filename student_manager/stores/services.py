from datetime import timedelta
from commons.exceptions import NotFoundException, ForbiddenException
from student_manager.users.models import User
from .models import (
    CartItem, 
    DeliveryAddress, 
    Product, 
    Store, 
    Cart, 
    StoreAddress, 
    Order
)
from django.db import transaction
from django.core.files import File
from django.utils import timezone

@transaction.atomic
def create_store(
    *, 
    user: User,
    image: File = None,
    name: str,
    url: str,
    email: str,
    address: str,
    city: str,
    province: str,
    landmark: str,
    longitude: int,
    latitude: int
) -> Store:
    store = Store.objects.create(
        user=user,
        image=image,
        name=name,
        url=url,
        email=email,
        address=address,
        city=city,
        province=province,
        landmark=landmark,
        longitude=longitude,
        latitude=latitude
    )

    return store

def create_cart(
    *,
    owner: User,
    store: Store,
    ordering_for_id: int
):
    if ordering_for_id:
        try:
            user_check = User.objects.get(pk=ordering_for_id)
        except:
            raise NotFoundException({"message": "not found exception"})
    cart = Cart.objects.create(owner=owner,
        store=store,
        ordering_for=user_check
    )
    return cart

def update_cart(
    *,
    cart: Cart,
    ordering_for: User,
    owner: User
) -> Cart:
    cart.ordering_for = ordering_for
    cart.owner = owner
    cart.save()
    return cart

def add_item(
    *,
    cart: Cart,
    user: User = None,
    product: Product,
    quantity: int
) -> CartItem:
    cart_data = CartItem.objects.filter(cart=cart, product=product).first()

    if cart_data:
        cart_data.quantity += quantity
        cart_data.save()
    else:
        cart_data = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity
        )

    return cart_data

def create_product(
    *,
    name: str,
    brand: str,
    description: str,
    average_cost: int,
    status: str,
    sellable: bool
) -> Product:
    product = Product.objects.create(
        name=name,
        brand=brand,
        description=description,
        average_cost=average_cost,
        status=status,
        sellable=sellable
    )
    return product

def delete_item(
    *,
    cart: Cart,
    user: User,
    product: Product
) -> CartItem:
    owner = cart.owner
    if user != owner:
        raise ForbiddenException()
    CartItem.objects.filter(cart=cart, product=product).delete()

def set_order_delivery_date(*, order:Order) -> Order:
    if not order.approved_at:
        return order
    # TODO: logic being failed
    delivery_date = order.approved_at + timedelta(weeks=1)
    order.estimated_delivery_date = delivery_date
    order.save()

def create_order(
    *,
    user: User,
    store: Store,
    cart: Cart,
    delivery_method: Order.DeliveryMethod,
    store_address: StoreAddress,
    delivery_address: DeliveryAddress,
    status: Order.OrderStatus
) -> Order:
    approved_at = None
    if status == Order.OrderStatus.FOR_PROCESSING:
        approved_at = timezone.now()

    order = Order.objects.create(
        user=user,
        store=store,
        cart=cart,
        delivery_method=delivery_method,
        delivery_address=delivery_address,
        store_address=store_address,
        status=status,
        approved_at=approved_at
    )

    set_order_delivery_date(order=order)
    order.total_cl_payable_amount = order.total_amount - order.total_cl_margin
    order.save()

    # apply promo
    
    return order
