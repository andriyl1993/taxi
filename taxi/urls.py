from django.conf.urls import url, include
from rest_framework import routers
from taxi_app import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns


urlpatterns = patterns('',
	url(r'^', include('taxi_app.urls')),
	url(r'^admin/', include(admin.site.urls)),
)  + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)