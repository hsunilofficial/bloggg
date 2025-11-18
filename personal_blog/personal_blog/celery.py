import multiprocessing
multiprocessing.set_start_method('spawn', force=True)

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_blog.settings')

app = Celery('personal_blog')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
