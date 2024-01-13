from django.contrib import admin
from .models import RoomType, Room, Service


admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Service)