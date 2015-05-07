# ~*~ coding: utf-8 ~*~

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as outlog
from models import *
#from serializers import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import datetime
import json
from forms import ImageForm
from collections import defaultdict
import simplejson

from django.views.generic import TemplateView

def index(request):
	try:
		print request.user 
		if request.user.is_authenticated():
		 	user2 = ClientUser.objects.filter(client_user = request.user)
			if not user2:
				user2 = DriverUser.objects.filter(user = request.user)
			return render(request, 'index.html', {'user2': user2[0], 'driver': json.dumps(user2[0].to_json())})
		return render(request, 'index.html')
	except Exception, e:
		print str(e)
		logout(request)
		return render(request, 'index.html')

def show_map(request):
	return render(request, 'map.html')

############registaration and authorization#############################

def sign_up(request):
	return render(request, 'Signup.html')

def logging(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			try:
				user2 = ClientUser.objects.get(client_user = user)
			except:
				user2 = DriverUser.objects.get(user = user)
				user2.state = 0
			user2.is_authorized = True
			user2.save()
			return redirect('/')
		else:
			return redirect('sign_up/')
	else:
		return redirect('sign_up/')

def logout(request):
	try:
		user = ClientUser.objects.get(client_user = request.user)
	except:
		user = DriverUser.objects.get(user = request.user)
		#for test
		user.state = 2


	user.is_authorized = False
	user.save()
	outlog(request)
	return redirect('/')

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
		du.state = 2   #offline 
		du.rating = 0
		du.is_authorized = False
		user = User.objects.create_user(username = _username, password = _password,email = _email, first_name = _first_name, last_name = _last_name)
		user.save()
		du.user = User.objects.get(username = _username)

		adds = AddService()
		if request.POST.get('conditioner'):
			adds.conditioner = request.POST.get('conditioner')
		else:
			adds.conditioner = False
		adds.type_salon = int(request.POST.get('type_salon'))
		if request.POST.get('place_from_things'):
			adds.place_from_things = request.POST.get('place_from_things')
		else:
			adds.place_from_things = False
		adds.count_places = int(request.POST.get('count_places'))
		adds.save()
		du.add_service = adds
		loc = Location()
		loc.save()
		du.location = loc
		du.save()
		return redirect('/')
	except Exception, e:
		print str(e)
		try:
			cu = ClientUser()

			cu.rating = 0
			img = Document()
			try:
				img.docfile = request.POST['photo']
				img.save()
			except Exception, e:
				print "Photo err - " + str(e)
			cu.photo = img
			cu.is_authorized = False
			user = User.objects.create_user(username = _username, password = _password,email = _email, first_name = _first_name, last_name = _last_name)
			user.save()
			
			cu.client_user = user
			cu.save()
			return redirect('/')
		except Exception, e:
			return HttpResponse("error = " + str(e))

########################################################################

class OrderView(TemplateView):
    template_name = "order.html"


def post_my_position_in_interval(request):
	if request.user.is_authenticated():
		try:
			user = User.objects.get(username = str(request.user))
			driver = DriverUser.objects.get(user = user)
			location = driver.location
			if str(location) == "None":
				location = Location()
			location.x = float(request.POST['x'])
			location.y = float(request.POST['y'])
			location.save()
			driver.location = location
			driver.save()
		except Exception, e:
			return HttpResponse(str(e))
	return HttpResponse('ok')


#client_coords
def get_driver_to_order(request):
	#order
	order = Order()
	order.date = request.POST['datetime']
	
	loc_start = Location()
	loc_start.x = request.POST.get('x_start')
	loc_start.y = request.POST.get('y_start')
	address = request.POST.get('start').split(',')
	loc_start.city = address[0]
	loc_start.street = address[1]
	if len(address) > 2:
		loc_start.building = int(address[2])
	loc_start.save()
	order.start_location = loc_start
	loc_end = Location()
	loc_end.x = request.POST.get('x_end')
	loc_end.y = request.POST.get('y_end')
	address = request.POST.get('end').split(',')
	loc_end.city = address[0]
	loc_end.street = address[1]
	if len(address) > 2:
		loc_end.building = int(address[2])
	loc_end.save()
	order.end_location = loc_end

	order.state = 0

	time = request.POST.get('duration')
	time = time.split(' ')
	if len(time) > 1:
		hour = int(time[0])
		minutes = int(time[1])
		order.time_travel = hour * 60 + minutes
	else:
		minutes = int(time[0])
		order.time_travel = minutes
	order.long_travel = request.POST.get('distance')

	if request.POST.get('is_fast') != None:
		order.is_fast = True
	else:
		order.is_fast = False
	order.client = ClientUser.objects.get(client_user = request.user)
	
	print "is_fast = " + str(order.is_fast)

	ads = AddService()
	if request.POST.get('conditioner') != None:
		ads.conditioner = request.POST.get('conditioner')
	else:
		ads.conditioner = False	
	if request.POST.get('type_salon') != "":
		ads.type_salon = int(request.POST.get('type_salon'))
	else:
		ads.type_salon = 0
	if request.POST.get('place_from_things') != None:
		ads.place_from_things = request.POST.get('place_from_things')
	else:
		ads.place_from_things = False
	if request.POST.get('count_places') != "":
		ads.count_places = request.POST.get('count_places')
	else:	
		ads.count_places = 0
	
	ads.save()
	order.add_service = ads

	order.save()

	alldu = DriverUser.objects.all()

	#filter(location__x__gte = order.start_location.x - 0.1).filter(location__x__lte = order.start_location.x + 0.1).filter(location__y__gte = order.start_location.y - 0.1).filter(location__y__lte = order.start_location.y + 0.1)
	drivers = DriverUser.objects.filter(state = 0)


	if ads.conditioner == True:
		drivers = drivers.filter(add_service__conditioner = True)
	if ads.type_salon != 0:
		drivers = drivers.filter(add_service__type_salon = ads.type_salon)
	if ads.place_from_things == True:
		drivers = drivers.filter(add_service__place_from_things = True)
	if ads.count_places != 0:
		drivers = drivers.filter(add_service__count_places__gte = ads.count_places)
	############################################

	js_order = json.dumps(order.to_json())
	json_drivers = query_to_json(drivers)

	return render(request, "state_order.html", {'json_order': js_order, 'order': order, 'drivers': json_drivers})


def return_driver_data_result(request):
	try:
		data = request.POST.get('data')
		print data
		elems = data[1:-1].split('},{')
		i = 0
		results = []
		if len(elems) > 1:
			for e in elems:
				elems[i] = "{" + e + "}"
				results[i] = json.loads(elems[i])
				i += 1
		else:
			try:
				elems[0] = "{" + elems[0] + "}"
				results.append(yaml.safe_load(elems[0]))
			except Exception, e:
				print str(e)

		cost = 0
		costs = []
		drivers = []
		times = []
		lengths = []
		for r in results:
			try:
				print r
				driver = DriverUser.objects.get(user__username = r['username'])
				cost = driver.rate_km_city * float(r['distance'].replace(',', '.')) + float(r['distance_to_client'].replace(',', '.')) * driver.rate_without_client
				if cost < driver.rate_min:
					cost = driver.rate_min
				order = Order.objects.get(pk = r['order_pk'])
				drivers.append(r['username'])
				costs.append(cost)
				order.order_drivers += r['username'] + ","
				time = float(r['duration']) + float(r['duration_to_client'])
				leng = float(r['distance']) + float(r['distance_to_client'].replace(',', '.'))
				order.order_lengths += str(leng) + ","
				order.order_times += str(time) + ","
				times.append(time)
				lengths.append(leng)
				order.order_costs += str(cost) + ","
				order.save()
			except Exception, e:
				print "Exceptio = " + str(e)
		if order.is_fast == True:
			min_cost = min(costs)
			index_dr = costs.index(min_cost)
		else:
			min_time = min(times)
			index_dr = times.index(min_time)
		driv = drivers[index_dr]
		driver = DriverUser.objects.get(user__username = driv)
		order.driver = driver
		order.save()
		return HttpResponse(order.to_json())
	except Exception, e:
		print str(e)

def change_state(request):
	driver_name = request.POST.get('driver')
	driver = DriverUser.objects.get(user__username = driver_name)
	driver.state = int(request.POST.get('state'))
	driver.save()
	return HttpResponse("ok")

def driver_order(request):
	driver = DriverUser.objects.get(user__username = request.user)
	return render(request, "driver_orders.html", {"driver": driver})

def get_orders(request):
	try:
		driver = DriverUser.objects.get(user__username = request.user)
		orders = Order.objects.filter(driver = driver).filter(state = 0)
	except Exception, e:
		print str(e)
	return HttpResponse(query_to_json(orders))

def result_order(request):
	try:
		order = request.POST.get('order')
		result = request.POST.get('result')
		order = Order.objects.get(pk = order)
		if result == 'apply':
			order.driver = DriverUser.objects.get(user__username = request.user)
			order.cost = order.order_costs.split(',')[0]
			order.state = 1
			order.save()
		elif result == 'clear':
			old_driver = order.order_drivers.split(',')[0]
			order.order_drivers = order.order_drivers[len(old_driver) + 1:]
			order.order_lengths = order.order_drivers[len(order.order_lengths.split(',')[0]) + 1:]
			order.order_costs = order.order_costs[len(order.order_costs.split(',')[0]) + 1:]
			order.order_times = order.order_times[len(order.order_times.split(',')[0]) + 1:]
			if order.order_drivers.encode('ascii','ignore') != "":
				driver = order.order_drivers.splt(',')[0]
				driver = DriverUser.objects.get(user__username = driver)
				order.driver = driver
				order.state = 1
				order.save()
			else:
				order.state = 2
				order.save()
		return HttpResponse('ok')
	except Exception, e:
		print str(e)

def last_result(request):
	try:
		order = request.POST.get('order')
		order = Order.objects.get(pk = order)
		print "pk = " + str(order.pk)
		print "state = " + str(order.state)
		if order.state == 1:
			return HttpResponse(json.dumps({'status':'ok'}))
		elif order.state == 2:
			return HttpResponse(json.dumps({'status':'clear'}))
		else:
			return HttpResponse(json.dumps({'status':'wait'}))
	except Exception, e:
		print str(e)


def get_result_from_driver(request):
	try:
		client = ClientUser.objects.get(client_user__username = request.user)
		order = Order.objects.filter(client = client).last()
		print"order.pk=" + str(order.pk)
		print "order.state = " + str(order.state)
		if order.state == 0:
			return HttpResponse(json.dumps({'status': 'wait'}))
		elif order.state == 1:
			return HttpResponse(json.dumps({'status': 'apply', 'cost': order.cost}))
		elif order.state == 2:
			return HttpResponse(json.dumps({'status': 'clear'}))
		elif order.state == 3:
			return HttpResponse(json.dumps({'status': '3'}))
		else:
			print "error"
			print order.state
		
	except Exception, e:
		print str(e)

def apply(request):
	try:
		res = request.POST.get('res')
		client = request.user
		order = Order.objects.filter(client__client_user__username = client).last()
		print res
		print order
		if res == 'ok':
			order.state = 3
		else:
			order.state = 2
		order.save()
		return HttpResponse('ok')
	except Exception, e:
		print str(e)


states = {
	"0": "new",
	"1": "rejected",
	"2": "apply",
	"3": "driver apply",
}


def history(request):
	if request.user.is_authenticated():
		user = request.user
		print user
		client_or_driver = ""
		us = ClientUser.objects.filter(client_user__username = user)
		if len(us) < 1:
			us = DriverUser.objects.filter(user__username = user)
			orders = Order.objects.filter(driver = us)
			client_or_driver = "driver"
		else:
			orders = Order.objects.filter(client = us)
			client_or_driver = "client"
		state = [states[str(v.state)] for v in orders]
		result = []
		for i in range(0, len(orders)):
			r = []
			r.append(orders[i])
			r.append(state[i])
			result.append(r)
		return render(request, "history.html", {"result": result, "user_": client_or_driver})
	else:
		return HttpResponse("ERROR")

def rating(request):
	if request.user.is_authenticated():
		user = request.user
		us = ClientUser.objects.filter(client_user__username = user)
		if len(us) < 1:
			us = DriverUser.objects.filter(user__username = user)
			orders = Order.objects.filter(driver = us)
			ratings = DriverRating.objects.filter(driver__user = us)
		else:
			orders = Order.objects.filter(client = us)
			ratings = ClientRating.objects.filter(client__client_user__username = user)
		count_orders = len(ratings)
		rating = float(sum([r.value for r in ratings])) / float(count_orders)
		return render(request, "rating.html", {"ratings": ratings, "mark": rating})
	else:
		return HttpResponse("ERROR")
	

def mark_rating(request):
	try:
		if request.user.is_authenticated():
			user = request.user
			us = ClientUser.objects.filter(client_user__username = user)
			pk = request.POST.get("pk")
			order = Order.objects.get(pk = pk)
			if len(us) < 1:
				us = DriverUser.objects.filter(user__username = user)
				user = "driver"
			else:
				user = "client"
			if user == "driver":
				cr = ClientRating()
				cr.value = request.POST.get("value")
				cr.driver = order.driver
				cr.client = order.client
				cr.save()
				order.client_rating = cr
				order.save()
				return HttpResponse(json.dumps({'res':cr.value, 'pk': order.pk}))
			else:
				cr = DriverRating()
				cr.car_state = int(request.POST.get("car_state"))
				cr.order_execution = int(request.POST.get("order_execution"))
				cr.comfort = int(request.POST.get("comfort"))
				cr.driver = order.driver
				cr.client = order.client
				cr.avarage_value = (cr.order_execution + cr.comfort + cr.car_state) / 3
				cr.save()
				order.driver_rating = cr
				order.save()
				return HttpResponse(json.dumps({'res':cr.avarage_value, 'pk': order.pk}))
	except Exception, e:
		print str(e)

def add_to_favourite(request):
	try:
		if request.user.is_authenticated():
			user = request.user
			client = ClientUser.objects.get(client_user__username = user)
			order = Order.objects.get(pk = request.POST.get('pk'))
			if client.favourite_drivers.filter(pk = order.driver.pk):
				return HttpResponse(json.dumps({'status': 'driver already added'}))
			client.favourite_drivers.add(order.driver)
			client.save()
			return HttpResponse(json.dumps({'status': 'add'}))
		return HttpResponse(json.dumps({'status': 'error'}))
	except Exception, e:
		print str(e)

def favourite_drivers(request):
	try:
		if request.user.is_authenticated():
			fd = ClientUser.objects.get(client_user__username = request.user).favourite_drivers.all()
			return render(request, "favourite_drivers.html", {'fd': fd})
	except Exception, e:
		print str(e)
			