# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxi_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='client_rating',
            field=models.OneToOneField(blank=True, to='taxi_app.ClientRating'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='cost',
            field=models.FloatField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='driver',
            field=models.ForeignKey(to='taxi_app.DriverUser', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='driver_rating',
            field=models.OneToOneField(blank=True, to='taxi_app.DriverRating'),
            preserve_default=True,
        ),
    ]
