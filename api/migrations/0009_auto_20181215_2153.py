# Generated by Django 2.1.1 on 2018-12-15 16:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20181215_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weather_data',
            name='time_stamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 15, 21, 53, 13, 197036)),
        ),
    ]
