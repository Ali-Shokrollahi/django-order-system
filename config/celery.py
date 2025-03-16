import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.django.local")

app = Celery("django_order_system")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()