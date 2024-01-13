from django.urls import path
from hotel import guest_views, admin_views

urlpatterns = [
    #URLS FOR GUEST
    path('', guest_views.home, name= 'guest_home'),
    path('guest_base/', guest_views.base, name = 'guest_base'),
    path('guest_room/', guest_views.room, name = 'guest_room'),
    path('guest_service/', guest_views.service, name = 'guest_service'),
    path('guest_notify/', guest_views.notify, name = 'guest_notify'),

    #URLS FOR ADMIN
    path('admin_base/', admin_views.base, name = 'admin_base'),
    path('admin_dashboard/', admin_views.home, name= 'admin_dashboard'),
    path('admin_guest/', admin_views.guest, name = 'admin_guest'),
    path('add_guest/', admin_views.add_guest, name='add_guest'),
    path('edit_guest/<int:user_id>/', admin_views.edit_guest, name='edit_guest'),
    path('delete_guest/<int:user_id>/', admin_views.delete_guest, name='delete_guest'),
    path('admin_rooms/', admin_views.room, name = 'admin_rooms'),   
    path('admin_reservations/', admin_views.reservation, name = 'admin_reservations'),
    path('admin_services/', admin_views.service, name = 'admin_services'), 
]