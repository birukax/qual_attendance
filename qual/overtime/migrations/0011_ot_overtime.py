# Generated by Django 5.0 on 2024-03-26 09:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overtime', '0010_rename_days_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='ot',
            name='overtime',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='overtime.overtime'),
        ),
    ]
