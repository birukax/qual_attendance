# Generated by Django 5.0 on 2024-07-18 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0016_remove_leave_total_days_leave_half_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='total_days',
            field=models.FloatField(default=False),
        ),
    ]
