# Generated by Django 5.0 on 2024-04-11 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0025_attendance_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='recalculated',
            field=models.BooleanField(default=False),
        ),
    ]
