# Generated by Django 5.1.7 on 2025-05-13 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goalapp', '0027_goal_days_spent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='number_of_goals_completed',
        ),
    ]
