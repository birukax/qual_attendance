# Generated by Django 5.0 on 2024-09-05 09:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0031_onfield_created_by_alter_onfield_approved_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='compile_date',
            field=models.DateField(default=datetime.date(2024, 9, 5)),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('Complete', 'Complete'), ('Incomplete', 'Incomplete'), ('Absent', 'Absent'), ('Day Off', 'Day Off'), ('On Leave', 'On Leave'), ('On Field', 'On Field'), ('Holiday', 'Holiday')], max_length=10, null=True),
        ),
    ]
