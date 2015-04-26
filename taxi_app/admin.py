from django.contrib import admin
from models import *

admin.site.register(Order)
admin.site.register(DriverUser)
admin.site.register(ClientUser)
admin.site.register(Location)
admin.site.register(ClientRating)
admin.site.register(DriverRating)