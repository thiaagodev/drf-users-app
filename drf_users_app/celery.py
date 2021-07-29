import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_users_app.settings')
app = Celery('drf_users_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
