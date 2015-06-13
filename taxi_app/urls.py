from django.conf.urls import url
from taxi_app import views
from taxi_app.views import *

urlpatterns = [
	url(r'^$', index),
	url(r'^map/', show_map),
	url(r'^create_user/', register),
	url(r'^logging/', logging),
	url(r'^sign_up/', sign_up),
	url(r'^logout/', logout),
	url(r'^logout/', logout),
	url(r'^order/', OrderView.as_view()),
	url(r'^post_my_position_in_interval/', post_my_position_in_interval, name="post_my_position_in_interval"),
	url(r'^get_driver_to_order/', get_driver_to_order),
	url(r'^return_driver_data_result/', return_driver_data_result),
	url(r'^change_state/', change_state),
	url(r'^driver_order/', driver_order),
	url(r'^get_orders/', get_orders),
	url(r'^result_order/', result_order),
	url(r'^last_result/', last_result),
	url(r'^apply/', apply),
	url(r'^history/', history),
	url(r'^rating/', rating),
	url(r'^mark_rating/', mark_rating),
	url(r'^add_to_favourite/', add_to_favourite),
	url(r'^favourite_drivers', favourite_drivers),
	url(r'^driver_profile/', driver_profile),
	url(r'^client_profile/', client_profile),
	url(r'^profile_to_json/', profile_to_json),
	url(r'^regime/', regime),


	url(r'^get_result_from_driver/', get_result_from_driver),
	url(r'^change_client_data/', change_client_data),
]

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()