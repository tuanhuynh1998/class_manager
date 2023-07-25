from celery.utils.log import get_task_logger
from student_manager.users.services import send_mail_service
from celery import shared_task

logger = get_task_logger(__name__)

@shared_task
def send_invoice(content, email):
    email = "admin@gmail.com"
    send_mail_service(email=email, subject="Monthly Invoice", content=content)

# @shared_task
# def create_monthly_invoice():
    