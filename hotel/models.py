from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User






class RoomType(models.Model):
    """
    Model representing the type of room in the hotel.

    Attributes:
    - type_id (int): Primary key for the room type.
    - name (str): Name of the room type.
    - description (str): Description of the room type.
    - price (int): Price of the room type.
    - image (ImageField): Image representing the room type.

    Methods:
    - __str__: Returns the string representation of the room type.
    """
    type_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    price = models.IntegerField()
    image = models.ImageField(upload_to='images')  
  
    def __str__(self):  
     
        return self.name

class Room(models.Model):
    """
    Model representing a room in the hotel.

    Attributes:
    - room_id (int): Primary key for the room.
    - room_number (str): Room number.
    - room_type (ForeignKey): Reference to the associated RoomType.
    - is_available (bool): Indicates whether the room is available.
    - is_occupied (bool): Indicates whether the room is currently occupied.

    Methods:
    - __str__: Returns the string representation of the room.
    """
    room_id = models.IntegerField(default=True, primary_key=True)
    room_number = models.CharField(max_length=10)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):  
        return f"{self.room_number} -----: {self.room_type.name}"
    
class Service(models.Model):
    """
    Model representing a service offered by the hotel.

    Attributes:
    - name (str): Name of the service.
    - description (str): Description of the service.
    - price (int): Price of the service.
    - image (ImageField): Image representing the service.

    Methods:
    - __str__: Returns the string representation of the service.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    price = models.IntegerField()
    image = models.ImageField(upload_to='images')  
  
    def __str__(self):  
        return self.name
    
