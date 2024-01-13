from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

def login_user(request):
    """
    View for handling user login.

    Authenticates the user based on provided username and password.
    If authentication is successful, logs in the user and redirects them to the appropriate dashboard.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Rendered HTML response or a redirection to the appropriate dashboard.
    """
    error = None
    if request.method == 'POST':
        
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('guest_home')
        else:
            error = 'Incorrect Username or Password. Please try again.'
            return render(request, 'authenticate/login.html', {'error': error})
    else:
        return render(request, 'authenticate/login.html', {'error': error})

def logout_user(request):
    """
    View for handling user logout.

    Logs out the currently authenticated user.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Redirection to the guest home page.
    """

    logout(request)
    return redirect('guest_home')

def register_user(request):
    """
    View for handling user registration.

    If the request method is POST, processes the registration form data and registers a new user.
    If registration is successful, logs in the new user and redirects them to the guest home page.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Rendered HTML response or a redirection to the guest home page.
    """
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('guest_home')
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html', {'form': form})
