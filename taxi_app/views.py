# ~*~ coding: utf-8 ~*~

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as outlog
from models import *
#from serializers import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from datetime import datetime
import json
from forms import ImageForm
from collections import defaultdict
import simplejson

from django.views.generic import TemplateView
import yaml


driver_state = ['online','has order','offline']
type_salon = {u"Будь-який": "0", u"Бюджет": "1", u"Бізнес": "2", u"Джип": "3"}

def regime(request):
	return HttpResponse("ok")

def index(request):
	try:
		if request.user.is_authenticated():
		 	user2 = ClientUser.objects.filter(client_user = request.user)
			if not user2:
				user2 = DriverUser.objects.filter(user = request.user)
			return render(request, 'index.html', {'user2': user2[0], 'driver': json.dumps(user2[0].to_json())})
		return render(request, 'index.html')
	except Exception, e:
		print str(e)
		try:
			logout(request)
			return render(request, 'index.html')
		except:
			return render(request, 'error.html')

def show_map(request):
	try:
		return render(request, 'map.html')
	except:
		return render(request, 'error.html')

############registaration and authorization#############################

def sign_up(request):
	try:
		return render(request, 'Signup.html')
	except:
		return render(request, 'error.html')


def logging(request):
	if not request.POST:
		return redirect('/sign_up/')
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			try:
				user2 = ClientUser.objects.get(client_user = user)
			except:
				try:
					user2 = DriverUser.objects.get(user = user)
					user2.state = 0
				except:
					return redirect('/sign_up/')
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
		try:
			user = DriverUser.objects.get(user = request.user)
			#for test
			user.state = 2
		except Exception, e:
			print "logout = " + str(e)
			return redirect('/')


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
		if len(request.POST.get('rate_min')) > 0:
			du = DriverUser()
			if request.POST.get('photo_car'):
				photo_car = Document(docfile = request.POST['photo_car'])
				photo_car.save()
				du.photo_car = photo_car
			if request.POST.get('photo_driver_license'):
				photo_driver_license = Document(docfile = request.POST['photo_driver_license']) 
				photo_driver_license.save()
				du.photo_driver_license = photo_driver_license
			if request.POST.get('photo_car_license'):
				photo_car_license = Document(docfile = request.POST['photo_car_license'])
				photo_car_license.save()
				du.photo_car_license = photo_car_license
			du.rate_min = request.POST['rate_min']
			du.rate_km_hightway = request.POST['rate_km_hightway']
			du.rate_km_city = request.POST['rate_km_city']
			du.about_me = request.POST['about_me']
			if request.POST.get('coefficient_congestion') != "":
				du.coefficient_congestion = float(request.POST['coefficient_congestion'])
			else:
				du.coefficient_congestion  = 0
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
			
			typesal = request.POST.get('type_salon')
			adds.type_salon = type_salon[typesal]
			if request.POST.get('place_from_things'):
				adds.place_from_things = request.POST.get('place_from_things')
			else:
				adds.place_from_things = False
			adds.count_places = int(request.POST.get('count_places'))
			adds.save()
			print "this"

			du.add_service = adds
			loc = Location()
			loc.save()
			du.location = loc
			du.save()
			print "this"

			return redirect('/')
		else:	
			cu = ClientUser()
			cu.rating = 0
			img = Document()
			img.docfile = request.POST['photo']
			img.save()
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

import time as _time
from time import mktime

#client_coords
def get_driver_to_order(request):
	#order
	try:
		order = Order()
		#order.date = request.POST['datetime']
		
		date = request.POST.get('date')
		time_order = request.POST.get('time')

		date = datetime.fromtimestamp(mktime(_time.strptime(date + " " + time_order, "%Y-%m-%d %H:%M")))
		order.date = date

		loc_start = Location()
		loc_start.x = request.POST.get('x_start')
		loc_start.y = request.POST.get('y_start')
		address = request.POST.get('start').split(',')
		if loc_start.x == None:
			loc_start.city = address[0]
			loc_start.street = address[1]
			if len(address) > 2:
				loc_start.building = int(address[2])
		loc_start.save()
		order.start_location = loc_start
		loc_end = Location()
		loc_end.x = request.POST.get('x_end')
		loc_end.y = request.POST.get('y_end')
		if loc_end.x == None:
			address = request.POST.get('end').split(',')
			loc_end.city = address[0]
			loc_end.street = address[1]
			if len(address) > 2:
				loc_end.building = int(address[2])
		loc_end.save()
		order.end_location = loc_end

		order.state = 0
		try:
			time = request.POST.get('duration')
			print time
			time = time.split(' ')
			
			if len(time) > 1:
				hour = int(time[0])
				minutes = int(time[1])
				order.time_travel = hour * 60 + minutes
			else:
				minutes = int(time[0])
				order.time_travel = minutes
			#long_travel = int(request.POST.get('distance'))
			long_travel = request.POST.get('distance').replace(',', '.')
			order.long_travel = float(long_travel)
		except:
			order.time_travel = 0
			order.long_travel = 0
		
		if request.POST.get('is_fast') != None:
			order.is_fast = True
		else:
			order.is_fast = False
		order.client = ClientUser.objects.get(client_user = request.user)
		driver_name = request.POST.get('driver_name')
		ads = AddService()
		if request.POST.get('conditioner') != None:
			ads.conditioner = request.POST.get('conditioner')
		else:
			ads.conditioner = False	
		if int(request.POST.get('type_salon')) != 0:
			ads.type_salon = int(request.POST.get('type_salon'))
		else:
			ads.type_salon = 0
		if request.POST.get('place_from_things') != None:
			ads.place_from_things = request.POST.get('place_from_things')
		else:
			ads.place_from_things = False
		if request.POST.get('count_places') != "":
			ads.count_places = int(request.POST.get('count_places'))
		else:	
			ads.count_places = 0
		
		ads.save()
		order.add_service = ads
		if driver_name != "":
			driver = DriverUser.objects.filter(user__username = driver_name)
			order.driver = driver[0]
		#print "----------------------------------------++++++++++++++++++++++++++++++++++++++++"
		#print order.to_json()
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
		
		if driver_name == "":
			json_drivers = query_to_json(drivers)
		else:
			drivers = []
			drivers.append(order.driver)
			json_drivers = query_to_json(drivers)
			
		return render(request, "state_order.html", {'json_order': js_order, 'order': order, 'drivers': json_drivers})
	except Exception, e:
		print "Erorr Last = " + str(e)
		return render(request, "error.html")

def return_driver_data_result(request):
	try:
		data = request.POST.get('data')
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
				driver = DriverUser.objects.get(user__username = r['username'])
				print driver
				cost = driver.rate_km_city * float(r['distance']) + float(r['distance_to_client'].replace(',', '.')) * driver.rate_without_client
				if cost < driver.rate_min:
					cost = driver.rate_min
				print cost
				order = Order.objects.get(pk = r['order_pk'])
				order.cost = cost
				drivers.append(r['username'])
				costs.append(cost)
				order.order_drivers += r['username'] + ","
				time = float(r['duration']) + float(r['duration_to_client'])
				print time
				leng = float(r['distance']) + float(r['distance_to_client'].replace(',', '.'))
				order.order_lengths += str(leng) + ","
				order.order_times += str(time) + ","
				print order.order_times
				
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
	try:
		driver = DriverUser.objects.get(user__username = request.user)
		return render(request, "driver_orders.html", {"driver": driver})
	except:
		return render(request, "error.html")

def get_orders(request):
	try:
		driver = DriverUser.objects.get(user__username = request.user)
		orders = Order.objects.filter(driver = driver).filter(state = 0)
		print query_to_json(orders)
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
				driver = order.order_drivers.split(',')[0]
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
		if order.state == 3:
			return HttpResponse(json.dumps({'status':'ok'}))
		elif order.state == 2:
			return HttpResponse(json.dumps({'status':'clear'}))
		else:
			return HttpResponse(json.dumps({'status':'waitj'}))
	except Exception, e:
		print str(e)


def get_result_from_driver(request):
	try:
		client = ClientUser.objects.get(client_user__username = request.user)
		order = Order.objects.filter(client = client).last()
		#print"order.pk=" + str(order.pk)
		#print "order.state = " + str(order.state)
		if order.state == 0:
			return HttpResponse(json.dumps({'status': 'wait', 'order': order.to_json()}))
		elif order.state == 1:
			return HttpResponse(json.dumps({'status': 'apply', 'cost': order.cost}))
		elif order.state == 2:
			return HttpResponse(json.dumps({'status': 'clear'}))
		elif order.state == 3:
			return HttpResponse(json.dumps({'status': '3'}))
		else:
			print "error"
			
	except Exception, e:
		print str(e)

def apply(request):
	try:
		res = request.POST.get('res')
		client = request.user
		order = Order.objects.filter(client__client_user__username = client).last()
		print res
		if res == u'Так':
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
	try:
		if request.user.is_authenticated():
			user = request.user
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
	except:
		return render(request, "error.html")

def rating(request):
	try:
		if request.user.is_authenticated():
			user = request.user
			user_type = ""
			us = ClientUser.objects.filter(client_user__username = user)
			if len(us) < 1:
				us = DriverUser.objects.filter(user__username = user)
				user_type = "driver"
				orders = Order.objects.filter(driver = us)
				ratings = DriverRating.objects.filter(driver = us)
			else:
				orders = Order.objects.filter(client = us)
				user_type = "client"
				ratings = ClientRating.objects.filter(client__client_user__username = user)
			count_orders = len(ratings)
			rating = 0
			if count_orders > 0:
				if user_type == "client":
					rating = float(sum([r.value for r in ratings])) / float(count_orders)
				else:
					rating = float(sum([r.avarage_value for r in ratings])) / float(count_orders)
			return render(request, "rating.html", {"ratings": ratings, "mark": rating, "user_type": user_type})

		else:
			return HttpResponse("ERROR")
	except:
		return render(request, "error.html")

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
			return render(request, "favourite_drivers.html", {'fd': fd, 'states': driver_state})
	except Exception, e:
		print str(e)
		return render(request, "error.html")
			

def driver_profile(request):
	try:
		if request.path.split('/')[-1] != "":
			user = DriverUser.objects.get(user__username = request.path.split('/')[-1])
		else:
			user = DriverUser.objects.get(user__username = request.user.username)
		return render(request, "user_profile.html", {'useruser':user, "type_user": "driver"})
	except:
		return render(request, "error.html")

def client_profile(request):
	try:
		if request.path.split('/')[-1] != "":
			user = ClientUser.objects.get(client_user__username = request.path.split('/')[-1])
		else:
			user = ClientUser.objects.get(client_user__username = request.user.username)
		return render(request, "user_profile.html", {'useruser':user, "type_user": "client"})
	except:
		return render(request, "error.html")

def change_client_data(request):
	client = ClientUser.objects.get(client_user = request.user)
	user = User.objects.get(username = request.user.username)

	user.first_name = request.POST.get('first_name')
	user.last_name = request.POST.get('last_name')
	user.email = request.POST.get('email')
	if request.POST.get('password'):
		user.set_password(request.POST.get('password'))
	user.username = request.POST.get('username')
	user.save()
	
	if request.POST.get('photo'):
		client.photo.docfile = request.POST.get('photo')
		client.save()
	return redirect('/client_profile/')

def profile_to_json(request):
	user = request.POST.get('username')
	if request.POST.get('type_user') == 'driver':
		order = Order.objects.get(pk = int(request.POST.get('order_id')))
		user = order.driver
	else:
		user = ClientUser.objects.get(client_user__username = user)
	return HttpResponse(json.dumps(user.to_json()))