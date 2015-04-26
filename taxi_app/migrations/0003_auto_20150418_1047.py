# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxi_app', '0002_auto_20150418_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='client_rating',
            field=models.OneToOneField(null=True, blank=True, to='taxi_app.ClientRating'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='cost',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='driver',
            field=models.ForeignKey(blank=True, to='taxi_app.DriverUser', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='driver_rating',
            field=models.OneToOneField(null=True, blank=True, to='taxi_app.DriverRating'),
            preserve_default=True,
        ),
    ]
