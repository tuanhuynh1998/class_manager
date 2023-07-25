from django.urls import path
from . import views

urlpatterns = [
    path('pymupdf/', views.OcrInvoiceView.as_view(), name='ocr-pymupdf'),
]
