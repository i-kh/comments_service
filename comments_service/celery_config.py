import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comments_service.settings")

app = Celery('celery_config', broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',
             include=['comments_service.comment.tasks'])
