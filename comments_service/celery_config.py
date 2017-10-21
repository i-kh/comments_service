import os

from celery import Celery
from comments_service.settings import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comments_service.settings")

redis_host = str(config['redis']['host'])
redis_port = int(config['redis']['port'])
redis_db = int(config['redis']['db'])

app = Celery('celery_config',
             broker='redis://{redis_host}:{redis_port}/{redis_db}'.format(
                 redis_host=redis_host,
                 redis_port=redis_port,
                 redis_db=redis_db),
             backend='redis://{redis_host}:{redis_port}/{redis_db}'.format(
                 redis_host=redis_host,
                 redis_port=redis_port,
                 redis_db=redis_db),
             include=['comments_service.comment.tasks'])
