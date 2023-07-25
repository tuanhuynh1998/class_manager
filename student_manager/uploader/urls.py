from django.urls import path
from . import views

urlpatterns = [
    path('', views.save_file, name="upload-file-to-s3"),
    path('file/', views.UploadFile.as_view(), name="upload-file"),
    path('<str:pk>/invoice/', views.InvoiceView.as_view(), name="invoice-view"),
    # path('invoices/', views.InvoiceAPIView.as_view(), name="create-invoice"),
]
