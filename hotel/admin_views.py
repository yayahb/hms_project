from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, EditUserForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Room, RoomType
from reservation.models import Reservation, ServiceReservation
from datetime import date

def home(request):
    """
    View for rendering the administrator's dashboard.

    Retrieves statistics about guests, rooms, and room types and renders the dashboard page.

    Returns:
    - HttpResponse: Rendered HTML response.
    """
    guests= User.objects.exclude(is_superuser=True).count()
    rooms = Room.objects.count()
    available_rooms = Room.objects.filter(is_available=True).count()
    unavailable_rooms = Room.objects.filter(is_available=False).count()
    single_rooms = Room.objects.filter(room_type=1).count()
    double_rooms = Room.objects.filter(room_type=2).count()
    triple_rooms = Room.objects.filter(room_type=3).count()
    deluxe_rooms = Room.objects.filter(room_type=4).count()
    executive_suite = Room.objects.filter(room_type=5).count()
    presidential_suite = Room.objects.filter(room_type=6).count()

    context = {
        'guests': guests,
        'rooms': rooms,
        'available_rooms': available_rooms,
        'unavailable_rooms': unavailable_rooms,
        'single_rooms': single_rooms,
        'double_rooms': double_rooms,
        'triple_rooms': triple_rooms,
        'deluxe_rooms': deluxe_rooms,
        'executive_suite': executive_suite,
        'presidential_suite': presidential_suite,
    }
    return render(request, 'administrator/dashboard.html', context)


def base(request):
    """
    View for rendering the base template for the administrator.

    Returns:
    - HttpResponse: Rendered HTML response.
    """
    return render(request, 'administrator/base.html')


def guest(request):
    """
    View for rendering the guest page for the administrator.

    Retrieves all User objects and renders the guest page with the list of users.

    Returns:
    - HttpResponse: Rendered HTML response.
    """
    users = User.objects.all()
    return render(request, 'administrator/guest.html', {'users':users})


def add_guest(request):
    """
    View for rendering the page to add a new guest.

    If the request method is POST, processes the form data and creates a new user.
    Otherwise, renders the page with the form to add a new guest.

    Returns:
    - HttpResponse: Rendered HTML response.
    """
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_guest')
    else:
        form = CreateUserForm()
    return render(request, 'administrator/add_guest.html', {'form': form})


def edit_guest(request, user_id):
    """
    View for rendering the page to edit a guest's information.

    If the request method is POST, processes the form data and updates the user information.
    Otherwise, renders the page with the form to edit a guest.

    Returns:
    - HttpResponse: Rendered HTML response.
     """
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_guest')
    else:
        form = EditUserForm(instance=user)
    return render(request, 'administrator/edit_guest.html', {'form': form, 'user': user})


def delete_guest(request, user_id):
    """
    View for deleting a guest.

    Deletes the specified user and redirects to the guest page.

    Returns:
    - HttpResponse: Redirect response.
    """
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_guest')


def room(request):
    """
    View for rendering the room page for the administrator.

    Retrieves all Room objects and reservations and renders the page with room information.

    Returns:
    - HttpResponse: Rendered HTML response.
    """
    rooms = Room.objects.all()
    reservations = Reservation.objects.all()
            
    return render(request, 'administrator/rooms.html', {'rooms': rooms})


def reservation(request):
    """
    View for rendering the reservation page for the administrator.

    Retrieves all Reservation objects and renders the page with reservation information.

    Returns:
    - HttpResponse: Rendered HTML response.
    """
    rooms = Room.objects.all()
    reservations = Reservation.objects.all()
    
    return render(request, 'administrator/reservations.html', {'reservations': reservations})


def service(request):
    """
    View for rendering the service page for the administrator.

    Retrieves all ServiceReservation objects and renders the page with service reservation information.

    Returns:
    - HttpResponse: Rendered HTML response.
    """
    services = ServiceReservation.objects.all()

    return render(request, 'administrator/services.html', {'services': services})