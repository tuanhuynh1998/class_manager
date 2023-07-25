from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from .models import Upload
from student_manager.uploader.models import Invoice
from student_manager.users.models import User
from django.db import transaction

class PublicS3MediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    default_acl = 'public-read'
    location = 'media'

def file_upload(file):
    upload = Upload(file=file)
    upload.save()
    return upload.image_url

@transaction.atomic
def create_invoice(
    *, 
    date: str, 
    amount: str,
    user: User,
    number: str,
) -> Invoice:
    amount_number = float(amount[1:])
    invoice = Invoice.objects.create(
        user=user,
        invoice_number=number,
        invoice_date=date,
        invoice_amount=amount_number,
    )
    return invoice
