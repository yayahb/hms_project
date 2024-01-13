from django.shortcuts import render, redirect
from .models import RoomType, Service
from reservation.models import Reservation
from django.contrib import messages
from datetime import datetime, timedelta, date


def home(request):
    """
    View for rendering the home page.

    If the user is authenticated and is a superuser, redirects to the admin dashboard.
    Otherwise, renders the guest home page.

    Returns:
    - HttpResponse: Rendered HTML response.
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
    return render(request, 'guest/home.html')

def base(request):
    """
    View for rendering the base template.

    Returns:
    - HttpResponse: Rendered HTML response.
    """
    return render(request, 'guest/base.html')

def room(request):
    """
    View for rendering the room page.

    Retrieves all RoomType objects and renders the room page with the room types.

    Returns:
    - HttpResponse: Rendered HTML response.
    """
    room_types = RoomType.objects.all()
    return render(request, 'guest/room.html', {'room_types': room_types})

def service(request):
    """
    View for rendering the service page.

    Retrieves all Service objects and renders the service page with the available services.

    Returns:
    - HttpResponse: Rendered HTML response.
    """
    services = Service.objects.all()

    return render(request, 'guest/service.html', {'services': services})

def notify(request):
    """
    View for rendering the notification page.

    Checks for expiring reservations and displays a warning message for each expiring reservation.

    Returns:
    - HttpResponse: Rendered HTML response.
    """
    
    reservations = Reservation.objects.filter(guest=request.user)
    expiring_reservations = []
    today = date.today()

    for reservation in reservations:
        if today == reservation.end_date:
            messages.warning(request, f'Your reservation for Room {reservation.room.room_number} is about to expire.')
            expiring_reservations.append(reservation)

    request.session['expiring_reservations_count'] = len(expiring_reservations)

    return render(request, 'guest/notify.html')