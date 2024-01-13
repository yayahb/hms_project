from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    """
    Model representing a chat message between users.

    Attributes:
    - sender (ForeignKey): Reference to the user sending the message.
    - recipient (ForeignKey): Reference to the user receiving the message.
    - message (TextField): The content of the chat message.
    - timestamp (DateTimeField): The timestamp indicating when the message was sent.

    Methods:
    - __str__: Returns a string representation of the chat message.
    """
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.recipient}: {self.message}"

