# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxi_app', '0008_auto_20150419_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='long_travel',
            field=models.FloatField(),
            preserve_default=True,
        ),
    ]
