# Generated by Django 5.0 on 2024-01-23 11:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_alter_pattern_next'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pattern',
            name='next',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pattern', to='attendance.pattern'),
        ),
    ]
