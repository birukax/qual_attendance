# Generated by Django 5.0 on 2024-02-16 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0017_remove_attendance_absent_remove_attendance_day_off_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailyrecord',
            name='employees',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='worked_hours',
            field=models.DurationField(null=True),
        ),
    ]
