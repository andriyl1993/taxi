# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxi_app', '0002_auto_20150611_0355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientuser',
            name='photo',
            field=models.OneToOneField(null=True, blank=True, to='taxi_app.Document'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='driveruser',
            name='about_me',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
