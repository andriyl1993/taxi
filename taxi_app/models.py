# ~*~ coding: utf-8 ~*~

from django.db import models
from django.contrib.auth.models import User
import datetime
import json


class Document(models.Model):
	docfile = models.ImageField(upload_to='documents/%Y/%m/%d')


class Location(models.Model):
	x = models.FloatField(default = 0, blank=True, null=True)
	y = models.FloatField(default = 0, blank=True, null=True)
	city = models.CharField(max_length = 50, default = '', blank = True)
	street = models.CharField(max_length = 50, default = '', blank = True)
	building = models.CharField(max_length = 5, default = '', blank = True)

	def to_json(self):
		return {
			'x': self.x,
			'y': self.y,
			'city': self.city,
			'street': self.street,
			'building': self.building,
		}


class AddService(models.Model):
	conditioner = models.BooleanField(default = False)
	type_salon = models.IntegerField(default = 0)
	place_from_things = models.BooleanField(default = False)
	count_places = models.IntegerField(default = 4)

	def to_json(self):
		return {
			"conditioner": self.conditioner,
			"type_salon": self.type_salon,
			"place_from_things": self.place_from_things,
			"count_places": self.count_places,
		}


class DriverUser(models.Model):
	user = models.OneToOneField(User, default=None)
	photo_car = models.OneToOneField(Document, blank=True, related_name="photo_car" )
	photo_driver_license = models.OneToOneField(Document, blank=True, related_name="photo_driver_license")
	photo_car_license = models.OneToOneField(Document, blank=True, related_name="photo_car_license")
	rate_min = models.IntegerField()
	rate_without_client = models.IntegerField(default=0)
	rate_km_hightway = models.IntegerField()
	rate_km_city = models.IntegerField()
	about_me = models.TextField()
	coefficient_congestion = models.FloatField(default = 1)
	state = models.IntegerField()
	location = models.OneToOneField(Location, null=True)#, choices = locations, default = locations[0])
	date_registration = models.DateTimeField(auto_now_add=True, default = datetime.datetime.now)
	rating = models.IntegerField(default = 0)
	add_service = models.OneToOneField(AddService, default = None, null=True)
	is_authorized = models.BooleanField(default = False)

	def __str__(self):
		return self.user.username

	def to_json(self):
		return {
			"username": self.user.username,
			"x": self.location.x,
			"y": self.location.y,
		}


class ClientUser(models.Model):
	client_user = models.OneToOneField(User)
	rating = models.FloatField()
	photo = models.OneToOneField(Document, blank=True)
	date_registration = models.DateTimeField(auto_now_add=True)
	favourite_drivers = models.ManyToManyField(DriverUser)
	is_authorized = models.BooleanField(default = False)

	def __str__(self):
		return self.client_user.username

	def to_json(self):
		return {
			"username": self.client_user.username,
			"rating": self.rating,
			"date_registration": str(self.date_registration),
			"is_authorized": self.is_authorized,
		}


class Statistic(models.Model):
	count_orders = models.IntegerField()
	count_drivings = models.IntegerField()
	on_app = models.IntegerField()			#how many you was enter to app
	user = models.OneToOneField(User)


class ClientRating(models.Model):
	value = models.IntegerField()
	driver = models.ForeignKey(DriverUser)
	client = models.ForeignKey(ClientUser)


class DriverRating(models.Model):
	car_state = models.IntegerField()
	order_execution = models.IntegerField()
	comfort = models.IntegerField()
	client = models.ForeignKey(ClientUser)
	driver = models.ForeignKey(DriverUser)
	avarage_value = models.FloatField()


class Order(models.Model):
	date = models.DateTimeField()
	cost = models.FloatField(blank = True, null=True)
	start_location = models.OneToOneField(Location, related_name = 'start_location')
	end_location = models.OneToOneField(Location, related_name = 'end_location')
	client_rating = models.OneToOneField(ClientRating, blank=True, null=True)
	driver_rating = models.OneToOneField(DriverRating, blank=True, null=True)
	state = models.IntegerField()
	time_travel = models.IntegerField()
	long_travel = models.IntegerField()
	is_fast = models.BooleanField(default = True)
	driver = models.ForeignKey(DriverUser, blank = True, null=True)
	client = models.ForeignKey(ClientUser)
	add_service = models.OneToOneField(AddService, default=None)
	order_drivers = models.CharField(default= "", max_length = 1024)
	order_lengths = models.CharField(default = "", max_length = 1024)
	order_times = models.CharField(default = "", max_length = 1024)
	order_costs = models.CharField(default = "", max_length = 1024)

	def to_json(self):
		return {
			"pk": self.pk,
			"date": str(self.date),
			"cost": self.cost,
			"start_location": self.start_location.to_json(),
			"end_location": self.end_location.to_json(),
			"state": self.state,
			"time_travel": self.time_travel,
			"long_travel": self.long_travel,
			"is_fast": self.long_travel,
			"client": self.client.client_user.username,
			"add_service": self.add_service.to_json(),
			"order_drivers": self.order_drivers,
		}


class Comments(models.Model):
	client = models.ForeignKey(ClientUser)
	driver = models.ForeignKey(DriverUser)
	whom = models.IntegerField()
	date = models.DateTimeField(auto_now_add = True)
	order = models.ForeignKey(Order)


def query_to_json(data):
	mess = []
	for m in data:
		mess.append(m.to_json())
 	return json.dumps(mess)