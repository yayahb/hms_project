from django.shortcuts import render, get_object_or_404, redirect
from hotel.models import Room, RoomType, Service
from .models import Reservation, ServiceReservation
from django.contrib.auth.models import User
from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from django.db.models import Q





# ROOM RESERVATION VIEWS

def room_type_detail(request, room_type_id):
    """
    View to display details of a specific room type.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - room_type_id (int): The ID of the room type to display.

    Returns:
    - HttpResponse: Rendered HTML response displaying room type details.
    """
    room_type = RoomType.objects.get(pk=room_type_id)
    rooms = Room.objects.filter(room_type=room_type)
    reservations = Reservation.objects.all()
    today = date.today()
        
    
    return render(request, 'room/room_type_detail.html', {'room_type': room_type, 'rooms': rooms})


@login_required
def make_reservation(request, room_id):
    """
    View to handle the process of making a room reservation.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - room_id (int): The ID of the room to be reserved.

    Returns:
    - HttpResponse: Rendered HTML response or a redirection to the appropriate page.
    """
    room = Room.objects.get(pk=room_id)
    error_message = None
    
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        today = date.today()
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        if end_date_obj < today or start_date_obj > end_date_obj or start_date_obj < today:
            error_message = 'Invalid dates'
            return render(request, 'room/make_reservation.html', {'room': room, 'error_message': error_message})
        
        clashing_reservations = Reservation.objects.filter(
            room=room,
            start_date__lte=end_date,
            end_date__gte=start_date
        ).exclude(pk=request.POST.get('reservation_id'))
        
        if clashing_reservations.exists():
            error_message = 'The room is already reserved for the given dates.'
            return render(request, 'room/make_reservation.html', {'room': room, 'error_message': error_message})
        
        reservation = Reservation.objects.create(
            guest=request.user,
            room=room,
            start_date=start_date,
            end_date=end_date
        )
            
        room.save()

        if request.user.is_superuser:
            return redirect('admin_rooms')
        else:
            return redirect('view_reservations')
    else:
        return render(request, 'room/make_reservation.html', {'room': room})

    

@login_required
def cancel_reservation(request, reservation_id):
    """
    View to handle the cancellation of a reservation.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - reservation_id (int): The ID of the reservation to be canceled.

    Returns:
    - HttpResponse: Redirection to the reservations page.
    """
    reservation = Reservation.objects.get(pk=reservation_id)
    room = reservation.room
    
    if request.user == reservation.guest:
        room.save()
        reservation.delete()
        
        return redirect('view_reservations')
   

@login_required
def view_reservations(request):
    reservations = Reservation.objects.filter(guest=request.user)
    services = ServiceReservation.objects.filter(guest=request.user)
    return render(request, 'view_reservations.html', {'reservations': reservations, 'services': services})


@login_required
def update_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    error_message = None

    if request.method == 'POST':
        new_start_date = request.POST.get('start_date')
        new_end_date = request.POST.get('end_date')

        today = date.today()
        start_date_obj = datetime.strptime(new_start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(new_end_date, "%Y-%m-%d").date()

        if end_date_obj < today or start_date_obj > end_date_obj or start_date_obj < today:
            error_message = 'Invalid dates'
            return render(request, 'room/update_reservation.html', {'reservation': reservation, 'error_message': error_message})

        clashing_reservations = Reservation.objects.filter(
            room=reservation.room,
            start_date__lte=new_end_date,
            end_date__gte=new_start_date
        ).exclude(pk=reservation_id)

        if clashing_reservations.exists():
            error_message = 'The new reservation dates clash with an existing reservation.'
            return render(request, 'room/update_reservation.html', {'reservation': reservation, 'error_message': error_message})

        reservation.start_date = new_start_date
        reservation.end_date = new_end_date
        reservation.save()

        return redirect('view_reservations')

    return render(request, 'room/update_reservation.html', {'reservation': reservation})

    





# ADMIN RESERVATION VIEWS


@login_required
def admin_make_reservation(request, room_id):
    """
    View to handle the process of making a room reservation by an admin.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - room_id (int): The ID of the room to be reserved.

    Returns:
    - HttpResponse: Rendered HTML response or a redirection to the appropriate page.
    """
    room = Room.objects.get(pk=room_id)

    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        today = date.today()
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

        if end_date_obj < today or start_date_obj > end_date_obj or start_date_obj < today:
            return render(request, 'admin/admin_make_reservation.html', {'room': room, 'error_message': 'Invalid dates'})

        clashing_reservations = Reservation.objects.filter(
            room=room,
            start_date__lte=end_date,
            end_date__gte=start_date
        )

        if clashing_reservations.exists():
            # Delete the clashing reservations
            clashing_reservations.delete()

        reservation = Reservation.objects.create(
            guest=request.user,
            room=room,
            start_date=start_date,
            end_date=end_date
        )

        room.save()


        return redirect('admin_reservations')

    return render(request, 'admin/admin_make_reservation.html', {'room': room})




@login_required
def admin_cancel_reservation(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    room = reservation.room
    
    room.is_available = True
    room.is_occupied = False
    room.save()
    reservation.delete()
        
    return redirect('admin_reservations')






# SERVICE RESERVATION VIEWS

@login_required
def service_reservation(request, service_id):
    service = Service.objects.get(pk=service_id)

    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        reservation_date = request.POST.get('reservation_date')
        reservation_time = request.POST.get('reservation_time') 

        reservation = ServiceReservation.objects.create(
            guest=request.user,
            service=service,
            reservation_date=reservation_date,
            reservation_time=reservation_time
        )
            

        service.save()
        return redirect('view_reservations')
    
    return render(request, 'service/service_reservation.html', {'service':service})


@login_required
def update_service(request, service_id):
    service = get_object_or_404(ServiceReservation, pk=service_id)

    if request.method == 'POST':
        new_reservation_date = request.POST.get('reservation_date')
        new_reservation_time = request.POST.get('reservation_time')


        service.reservation_date = new_reservation_date
        service.reservation_time = new_reservation_time
        service.save()

        return redirect('view_reservations')

    return render(request, 'service/update_service.html', {'service': service})


@login_required
def cancel_service(request, service_id):
    service = get_object_or_404(ServiceReservation, pk=service_id)
    
    if request.user == service.guest:
        service.delete()
        
        return redirect('view_reservations')