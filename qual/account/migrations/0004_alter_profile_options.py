# Generated by Django 5.0 on 2024-03-21 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profile_employee'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'permissions': [('can_approve', 'Can Approve')]},
        ),
    ]
