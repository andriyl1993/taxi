from django.conf.urls import url, include
from rest_framework import routers
from taxi_app import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'clients', views.ClientUserViewSet)
router.register(r'drivers', views.DriverUserViewSet)
router.register(r'locations', views.LocationViewSet)
router.register(r'drivers_rating', views.DriverRatingViewSet)
router.register(r'users_rating', views.ClientRatingViewSet)
router.register(r'comments', views.CommentsViewSet)
router.register(r'statistics', views.StatisticViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'add_services', views.AddServicesViewSet)

urlpatterns = patterns('',
	url(r'^api/', include(router.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^', include('taxi_app.urls')),
	url(r'^admin/', include(admin.site.urls)),
)  + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)