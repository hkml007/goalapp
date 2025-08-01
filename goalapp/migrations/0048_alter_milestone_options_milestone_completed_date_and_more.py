# Generated by Django 5.1.7 on 2025-05-30 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goalapp', '0047_alter_milestone_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='milestone',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='milestone',
            name='completed_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='milestone',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
