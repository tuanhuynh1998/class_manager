from atexit import register
from django.contrib import admin
from .models import Store, Cart, Product, Order

admin.site.register(Store)
admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(Order)
