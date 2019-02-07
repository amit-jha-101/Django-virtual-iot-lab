# Generated by Django 2.1.4 on 2019-01-03 15:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190103_2042'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThingRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_sql', models.CharField(max_length=1000)),
                ('rule_name', models.CharField(max_length=255)),
                ('sensor_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.SensorData')),
            ],
        ),
        migrations.AlterField(
            model_name='weather_data',
            name='time_stamp',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 3, 20, 54, 45, 551616)),
        ),
    ]