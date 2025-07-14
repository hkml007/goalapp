import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goalproject.settings')
app = Celery('goalproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()



# proj/celery.py or settings.py
from celery.schedules import crontab

app.conf.beat_schedule = {
    'send-every-minute': {
        'task': 'reminders.tasks.send_due_reminders',
        'schedule': crontab(),   # every minute
    },
}
