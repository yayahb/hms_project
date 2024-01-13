from django.contrib import admin
from .models import Reservation, ServiceReservation
from django_cron.models import CronJobLog


admin.site.register(Reservation)
admin.site.register(ServiceReservation)