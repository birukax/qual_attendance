# Generated by Django 5.0 on 2024-02-05 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0002_rename_ending_date_leave_end_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leavetype',
            old_name='maximum_date',
            new_name='maximum_days',
        ),
    ]
