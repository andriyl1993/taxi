from django.conf.urls import url
from taxi_app import views
from taxi_app.views import *

urlpatterns = [
	url(r'^', index),
	url(r'^map/', show_map),
	url(r'^create_user/', register),
	url(r'logging/', logging),
	url(r'^sign_up/', sign_up),
	url(r'^logout/', logout),
	url(r'^route_data/', route_data),	
	url(r'^logout/', logout),
	#url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
]