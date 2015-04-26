# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxi_app', '0003_auto_20150418_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='x',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='y',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
    ]
