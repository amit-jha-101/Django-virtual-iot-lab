# Generated by Django 2.1.4 on 2019-01-14 18:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CronData',
            fields=[
                ('SensorName', models.CharField(default=uuid.uuid4, max_length=255, primary_key=True, serialize=False)),
                ('testTime', models.IntegerField()),
                ('testStatus', models.CharField(default='off', max_length=255)),
            ],
        ),
    ]