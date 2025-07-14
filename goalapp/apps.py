
from django.apps import AppConfig
import sys

class GoalappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'goalapp'

    def ready(self):
        if 'runserver' in sys.argv or 'runserver_plus' in sys.argv:
            from goalapp.reminder_scheduler import start_scheduler
            start_scheduler()
