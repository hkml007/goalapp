from django.contrib import admin

# Register your models here.

from .models import DailyReminder

admin.site.register(DailyReminder)
