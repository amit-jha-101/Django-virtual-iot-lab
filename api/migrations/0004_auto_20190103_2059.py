# Generated by Django 2.1.4 on 2019-01-03 15:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190103_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thingrules',
            name='sensor_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='weather_data',
            name='time_stamp',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 3, 20, 59, 32, 566387)),
        ),
    ]
