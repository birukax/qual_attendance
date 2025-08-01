# Generated by Django 5.0 on 2024-03-13 11:10

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shift', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='current_pattern',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_shift', to='shift.pattern'),
        ),
        migrations.AddField(
            model_name='shift',
            name='last_updated',
            field=models.DateField(default=datetime.datetime(2024, 1, 1, 0, 0)),
        ),
    ]
