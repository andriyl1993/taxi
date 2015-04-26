# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AddService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('conditioner', models.BooleanField(default=False)),
                ('type_salon', models.IntegerField(default=0)),
                ('place_from_things', models.BooleanField(default=False)),
                ('count_places', models.IntegerField(default=4)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.FloatField()),
                ('date_registration', models.DateTimeField(auto_now_add=True)),
                ('is_authorized', models.BooleanField(default=False)),
                ('client_user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('whom', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(to='taxi_app.ClientUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.ImageField(upload_to=b'documents/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DriverRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('car_state', models.IntegerField()),
                ('order_execution', models.IntegerField()),
                ('comfort', models.IntegerField()),
                ('avarage_value', models.FloatField()),
                ('client', models.ForeignKey(to='taxi_app.ClientUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DriverUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate_min', models.IntegerField()),
                ('rate_without_client', models.IntegerField(default=0)),
                ('rate_km_hightway', models.IntegerField()),
                ('rate_km_city', models.IntegerField()),
                ('about_me', models.TextField()),
                ('coefficient_congestion', models.FloatField(default=1)),
                ('state', models.IntegerField()),
                ('date_registration', models.DateTimeField(default=datetime.datetime.now, auto_now_add=True)),
                ('rating', models.IntegerField(default=0)),
                ('is_authorized', models.BooleanField(default=False)),
                ('add_service', models.OneToOneField(null=True, default=None, to='taxi_app.AddService')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.FloatField(default=0, blank=True)),
                ('y', models.FloatField(default=0, blank=True)),
                ('city', models.CharField(default=b'', max_length=50, blank=True)),
                ('street', models.CharField(default=b'', max_length=50, blank=True)),
                ('building', models.CharField(default=b'', max_length=5, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('cost', models.FloatField()),
                ('state', models.IntegerField()),
                ('time_travel', models.IntegerField()),
                ('long_travel', models.IntegerField()),
                ('is_fast', models.BooleanField(default=True)),
                ('add_service', models.OneToOneField(default=None, to='taxi_app.AddService')),
                ('client', models.ForeignKey(to='taxi_app.ClientUser')),
                ('client_rating', models.OneToOneField(to='taxi_app.ClientRating')),
                ('driver', models.ForeignKey(to='taxi_app.DriverUser')),
                ('driver_rating', models.OneToOneField(to='taxi_app.DriverRating')),
                ('end_location', models.OneToOneField(related_name='end_location', to='taxi_app.Location')),
                ('start_location', models.OneToOneField(related_name='start_location', to='taxi_app.Location')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count_orders', models.IntegerField()),
                ('count_drivings', models.IntegerField()),
                ('on_app', models.IntegerField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='driveruser',
            name='location',
            field=models.OneToOneField(null=True, to='taxi_app.Location'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='driveruser',
            name='photo_car',
            field=models.OneToOneField(related_name='photo_car', blank=True, to='taxi_app.Document'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='driveruser',
            name='photo_car_license',
            field=models.OneToOneField(related_name='photo_car_license', blank=True, to='taxi_app.Document'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='driveruser',
            name='photo_driver_license',
            field=models.OneToOneField(related_name='photo_driver_license', blank=True, to='taxi_app.Document'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='driveruser',
            name='user',
            field=models.OneToOneField(default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='driverrating',
            name='driver',
            field=models.ForeignKey(to='taxi_app.DriverUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='driver',
            field=models.ForeignKey(to='taxi_app.DriverUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='order',
            field=models.ForeignKey(to='taxi_app.Order'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientuser',
            name='favourite_drivers',
            field=models.ManyToManyField(to='taxi_app.DriverUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientuser',
            name='photo',
            field=models.OneToOneField(blank=True, to='taxi_app.Document'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientrating',
            name='client',
            field=models.ForeignKey(to='taxi_app.ClientUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientrating',
            name='driver',
            field=models.ForeignKey(to='taxi_app.DriverUser'),
            preserve_default=True,
        ),
    ]
