from django.db import models
from hotel.models import Room, Service
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import time, datetime
from django.core.exceptions import ValidationError

def start_time():
    """
    Utility function to get the default start time for reservations.

    Returns:
    - time: The default start time for reservations.
    """
    now = datetime.now()
    time = now.time()
    start = time.replace(hour=0, minute=0, second=0, microsecond=0)
    return start


def end_time():
    """
    Utility function to get the default end time for reservations.

    Returns:
    - time: The default end time for reservations.
    """
    now = datetime.now()
    time = now.time()
    start = time.replace(hour=12, minute=0, second=0, microsecond=0)
    return start

class Reservation(models.Model):
    """
    Model representing a reservation for a room.

    Attributes:
    - guest (ForeignKey): Reference to the user making the reservation.
    - room (ForeignKey): Reference to the room being reserved.
    - start_date (DateField): The start date of the reservation.
    - start_time (TimeField): The start time of the reservation.
    - end_date (DateField): The end date of the reservation.
    - end_time (TimeField): The end time of the reservation.

    Methods:
    - __str__: Returns a string representation of the reservation.
    - duration: Property that calculates the duration of the reservation in days.

    Meta:
    - ordering: Orders reservations by start date.
    """
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField(default=start_time)
    end_date = models.DateField()
    end_time = models.TimeField(default=end_time)


    def __str__(self):
        return f"Guest: {self.guest.username} - Room: {self.room.room_number} "
    
    @property
    def duration(self):
        return (self.end_date - self.start_date).days
    
    class Meta:
        ordering = ['start_date']

    
    
class ServiceReservation(models.Model):
    """
    Model representing a reservation for a service.

    Attributes:
    - guest (ForeignKey): Reference to the user making the service reservation.
    - service (ForeignKey): Reference to the service being reserved.
    - reservation_date (DateField): The date of the service reservation.
    - reservation_time (TimeField): The time of the service reservation.

    Methods:
    - __str__: Returns a string representation of the service reservation.
    """
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()

    def __str__(self):
        return f"Service: {self.service.name} - Guest: {self.guest.username}"
    
    