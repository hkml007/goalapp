# Generated by Django 5.1.5 on 2025-06-13 09:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goalapp', '0050_milestone_completed_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='AIInsight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generated_on', models.DateTimeField(auto_now_add=True)),
                ('feedback_summary', models.TextField(help_text='Personalized analysis or insight')),
                ('motivational_message', models.TextField(help_text='Tailored motivational prompt')),
                ('strategy_suggestion', models.TextField(help_text='Recommended strategy for overcoming roadblocks')),
                ('performance_score', models.FloatField(default=0.0, help_text='Numeric performance metric (0-100)')),
                ('milestone_accuracy', models.FloatField(default=0.0, help_text='Milestone completion rate')),
                ('reviewed', models.BooleanField(default=False, help_text='Whether user has seen this insight')),
                ('goal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='goalapp.goal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goalapp.login')),
            ],
            options={
                'ordering': ['-generated_on'],
            },
        ),
    ]
