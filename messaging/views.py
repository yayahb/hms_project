from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import ChatMessage
from .forms import ChatForm

@login_required
def chat(request, recipient_id):
    """
    View for rendering and handling chat messages with a specific recipient.

    Retrieves chat messages between the logged-in user and the specified recipient.
    Handles the submission of new chat messages.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - recipient_id (int): The ID of the recipient User.

    Returns:
    - HttpResponse: Rendered HTML response or a redirection to the chat page.
    """
    recipient = get_object_or_404(User, id=recipient_id)
    messages = ChatMessage.objects.filter(sender=request.user, recipient=recipient) | ChatMessage.objects.filter(sender=recipient, recipient=request.user)
    messages = messages.order_by('timestamp')
    if request.method == 'POST':
        
        message = request.POST["message"]
        chat_message = ChatMessage(sender=request.user, recipient=recipient, message=message)
        chat_message.save()
        return redirect('chat', recipient_id=recipient_id)
    else:
        return render(request, 'chat.html', {'recipient': recipient, 'messages': messages})


@login_required
def chat_list(request):
    """
    View for rendering the list of chat contacts.

    Retrieves a list of users with whom the logged-in user has exchanged chat messages.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Rendered HTML response.
    """
    chats = ChatMessage.objects.filter(sender=request.user).values_list('recipient', flat=True).distinct()
    chats = [get_object_or_404(User, id=chat_id) for chat_id in chats]
    return render(request, 'chat_list.html', {'chats': chats})
