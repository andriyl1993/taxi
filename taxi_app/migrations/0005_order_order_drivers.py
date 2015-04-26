# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxi_app', '0004_auto_20150418_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_drivers',
            field=models.CharField(max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
    ]
