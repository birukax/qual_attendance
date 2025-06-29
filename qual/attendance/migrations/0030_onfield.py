# Generated by Django 5.0 on 2024-08-14 11:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0029_dailyrecord_device'),
        ('employee', '0020_employee_old_rule_balance'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OnField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('total_days', models.FloatField(blank=True, null=True)),
                ('reason', models.FloatField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('rejected', models.BooleanField(default=False)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='on_field_approval', to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='on_fields', to='employee.employee')),
                ('rejected_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='on_field_rejection', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
