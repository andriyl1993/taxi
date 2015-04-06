from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as outlog
from rest_framework import viewsets
from models import *
from serializers import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import render, redirect
import datetime
from forms import ImageForm


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class ClientUserViewSet(viewsets.ModelViewSet):
	queryset = ClientUser.objects.all()
	serializer_class = ClientUserSerializer


class DriverUserViewSet(viewsets.ModelViewSet):
	queryset = DriverUser.objects.all()
	serializer_class = DriverUserSerializer


class LocationViewSet(viewsets.ModelViewSet):
	queryset = Location.objects.all()
	serializer_class = LocationSerializer


class StatisticViewSet(viewsets.ModelViewSet):
	queryset = Statistic.objects.all()
	serializer_class = StatisticSerializer


class OrderViewSet(viewsets.ModelViewSet):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer


class DriverRatingViewSet(viewsets.ModelViewSet):
	queryset = DriverRating.objects.all()
	serializer_class = DriverRatingSerializer


class ClientRatingViewSet(viewsets.ModelViewSet):
	queryset = ClientRating.objects.all()
	serializer_class = ClientRatingSerializer


class CommentsViewSet(viewsets.ModelViewSet):
	queryset = Comments.objects.all()
	serializer_class = CommentsSerializer

class AddServicesViewSet(viewsets.ModelViewSet):
	queryset = AddService.objects.all()
	serializer_class = AddServiceSerializer

def index(request):
	return render(request, 'index.html')

def show_map(request):
	return render(request, 'map.html')

def sign_up(request):
	return render(request, 'Signup.html')

def logging(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return redirect('/map/')
		else:
			return redirect('sign_up/')
	else:
		return redirect('sign_up/')


def logout(request):
	outlog(request)
	return redirect('/')

def route_data(request):
	distance = request.POST['distance']
	duration = request.POST['duration']
	print "distance = " + distance
	return HttpResponse("ok")

def register(request):
	_username = request.POST['username']
	try:
		user = User.objects.get(username = _username)
		return HttpResponse('bad username')
	except:
		_password = request.POST['password']
		_email = request.POST['email']
		_first_name = request.POST['first_name']
		_last_name = request.POST['last_name']
	
		user = User.objects.create_user(username = _username, password = _password,email = _email, first_name = _first_name, last_name = _last_name)
		user.save()
	try:
		du = DriverUser()
		photo_car = Document(docfile = request.POST['photo_car'])
		photo_car.save()
		du.photo_car = photo_car
		photo_driver_license = Document(docfile = request.POST['photo_driver_license']) 
		photo_driver_license.save()
		du.photo_driver_license = photo_driver_license
		photo_car_license = Document(docfile = request.POST['photo_car_license'])
		photo_car_license.save()
		du.photo_car_license = photo_car_license
		du.rate_min = request.POST['rate_min']
		du.rate_km_hightway = request.POST['rate_km_hightway']
		du.rate_km_city = request.POST['rate_km_city']
		du.about_me = request.POST['about_me']
		du.coefficient_congestion = request.POST['coefficient_congestion']
		du.state = request.POST['state']
		du.location = request.POST['location']
		du.rating = 0
		du.is_authorized = False
		du.save()
	except:
		try:
			cu = ClientUser()

			cu.client_user = user
			cu.rating = 0
			img = Document()
			try:
				img.docfile = request.POST['photo']
				img.save()
			except Exception, e:
				print "Photo err - " + str(e)
			cu.photo = img
			cu.is_authorized = False
			cu.save()
		except Exception, e:
			return HttpResponse("error = " + str(e))
	return HttpResponse('register')