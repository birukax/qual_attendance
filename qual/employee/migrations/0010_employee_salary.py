# Generated by Django 5.0 on 2024-03-16 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0009_alter_employee_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='salary',
            field=models.FloatField(null=True),
        ),
    ]
