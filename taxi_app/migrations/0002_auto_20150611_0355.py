# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxi_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driveruser',
            name='coefficient_congestion',
            field=models.FloatField(default=1, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='driveruser',
            name='photo_car',
            field=models.OneToOneField(related_name='photo_car', null=True, blank=True, to='taxi_app.Document'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='driveruser',
            name='photo_car_license',
            field=models.OneToOneField(related_name='photo_car_license', null=True, blank=True, to='taxi_app.Document'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='driveruser',
            name='photo_driver_license',
            field=models.OneToOneField(related_name='photo_driver_license', null=True, blank=True, to='taxi_app.Document'),
            preserve_default=True,
        ),
    ]
