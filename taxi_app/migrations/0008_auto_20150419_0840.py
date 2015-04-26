# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxi_app', '0007_auto_20150419_0749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_costs',
            field=models.CharField(default=b'', max_length=1024),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_drivers',
            field=models.CharField(default=b'', max_length=1024),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_lengths',
            field=models.CharField(default=b'', max_length=1024),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_times',
            field=models.CharField(default=b'', max_length=1024),
            preserve_default=True,
        ),
    ]
