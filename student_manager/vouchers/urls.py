from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateVoucherAPIView.as_view(), name="create-voucher"),
]
