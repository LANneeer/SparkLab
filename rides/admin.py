from django.contrib import admin

from rides.models import Ride, RideRequest

admin.site.register(Ride)
admin.site.register(RideRequest)
