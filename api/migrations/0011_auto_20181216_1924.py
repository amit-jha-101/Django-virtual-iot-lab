# Generated by Django 2.1.1 on 2018-12-16 13:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20181215_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weather_data',
            name='time_stamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 16, 19, 24, 56, 733327)),
        ),
    ]
