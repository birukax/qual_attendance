# Generated by Django 5.0 on 2024-02-26 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overtime', '0002_overtimetype_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overtime',
            name='end_time_actual',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='overtime',
            name='start_time_actual',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='overtime',
            name='total_rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='overtimetype',
            name='day_span',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='overtimetype',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
