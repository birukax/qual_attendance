# Generated by Django 5.0 on 2024-03-20 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0012_employee_annual_leave_balance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='termination_date',
            field=models.DateField(null=True),
        ),
    ]
