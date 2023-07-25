from django.contrib import admin
from .models import Upload, Invoice, Payment

admin.site.register(Upload)
admin.site.register(Invoice)
admin.site.register(Payment)
