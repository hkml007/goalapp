# Generated by Django 5.1.7 on 2025-05-30 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goalapp', '0048_alter_milestone_options_milestone_completed_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='milestone',
            options={},
        ),
        migrations.RemoveField(
            model_name='milestone',
            name='completed_date',
        ),
        migrations.RemoveField(
            model_name='milestone',
            name='order',
        ),
    ]
