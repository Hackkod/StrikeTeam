from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'striketeam.settings')
app = Celery('striketeam')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'display-image-every-100-seconds': {
        'task': 'team.tasks.display_image_task',
        'schedule': 100.0,  # каждые 100 секунд
    },
}