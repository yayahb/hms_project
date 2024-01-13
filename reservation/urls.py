from django.urls import path, include
from reservation import views

urlpatterns = [
    #ROOM URLS
     path('room-type/<int:room_type_id>/', views.room_type_detail, name='room_type_detail'),
     path('make-reservation/<int:room_id>/', views.make_reservation, name='make_reservation'),
     path('view-reservations/', views.view_reservations, name='view_reservations'),
     path('update-reservation/<int:reservation_id>/', views.update_reservation, name='update_reservation'),
     path('cancel-reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),


     #ADMIN URLS
     path('admin-make-reservation/<int:room_id>/', views.admin_make_reservation, name='admin_make_reservation'),
     path('admin-cancel-reservation/<int:reservation_id>/', views.admin_cancel_reservation, name='admin_cancel_reservation'),


     #SERVICE URLS
     path('service-reservation/<int:service_id>/', views.service_reservation, name='service_reservation'),
     path('update-service/<int:service_id>/', views.update_service, name='update_service'),
     path('cancel-service/<int:service_id>/', views.cancel_service, name='cancel_service'),


     
]