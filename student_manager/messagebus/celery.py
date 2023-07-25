import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_training.settings")

app = Celery("student_manager")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.timezone = 'UTC'
# app.conf.beat_schedule = {
#     'send_monthly_invoice': {
#         'task': 'send_invoice'
#     }
# }
