from django.db import models
from django.contrib.auth.models import User
import datetime

#from views import get_all_locations

class Document(models.Model):
	docfile = models.ImageField(upload_to='documents/%Y/%m/%d')

class Location(models.Model):
	x = models.FloatField(default = 0, blank = True)
	y = models.FloatField(default = 0, blank = True)
	city = models.CharField(max_length = 50, default = '', blank = True)
	street = models.CharField(max_length = 50, default = '', blank = True)
	building = models.CharField(max_length = 5, default = '', blank = True)


#locations = sorted((item, item) for item in get_all_locations())


class AddService(models.Model):
	conditioner = models.BooleanField(default = False)
	type_salon = models.IntegerField(default = 0)
	place_from_things = models.BooleanField(default = False)
	count_places = models.IntegerField(default = 4)


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
	location = models.OneToOneField(Location)#, choices = locations, default = locations[0])
	date_registration = models.DateTimeField(auto_now_add=True, default = datetime.datetime.now)
	rating = models.IntegerField(default = 0)
	add_service = models.OneToOneField(AddService, default = None)
	is_authorized = models.BooleanField(default = False)


class ClientUser(models.Model):
	client_user = models.OneToOneField(User)
	rating = models.FloatField()
	photo = models.OneToOneField(Document, blank=True)
	date_registration = models.DateTimeField(auto_now_add=True)
	favourite_drivers = models.ManyToManyField(DriverUser)
	is_authorized = models.BooleanField(default = False)

	# def save(self, *args, **kwargs):
	# 	self.user.id = self.id
 #        super(User, self).save(*args, **kwargs)


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
	cost = models.FloatField()
	start_location = models.OneToOneField(Location, related_name = 'start_location')
	end_location = models.OneToOneField(Location, related_name = 'end_location')
	client_rating = models.OneToOneField(ClientRating)
	driver_rating = models.OneToOneField(DriverRating)
	state = models.IntegerField()
	time_travel = models.IntegerField()
	long_travel = models.IntegerField()
	is_fast = models.BooleanField(default = True)
	driver = models.ForeignKey(DriverUser)
	client = models.ForeignKey(ClientUser)
	add_service = models.OneToOneField(AddService, default=None)


class Comments(models.Model):
	client = models.ForeignKey(ClientUser)
	driver = models.ForeignKey(DriverUser)
	whom = models.IntegerField()
	date = models.DateTimeField(auto_now_add = True)
	order = models.ForeignKey(Order)
