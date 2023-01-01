from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm


def login(request):
    """Log in an existing user"""
    if request.method != 'POST':
        # Display a blank login form:
        form = LoginForm()
    else:
        # Process completed form.
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            django_login(request, user)
            # Bring a logged-in user to the home page.
            return redirect('expense_tracker_app:index')

    context = {'form': form}
    return render(request, 'login.html', context)


def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display a blank registration form.
        form = UserCreationForm()
    else:
        # Process completed form.
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to home page.
            django_login(request, new_user)
            return redirect('expense_tracker_app:index')
    # Display a blank or invalid form.
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    context = {'form': form}
    return render(request, 'register.html', context)


def logout(request):
    """Function taking care of a user which just logged out."""
    if request.user.is_authenticated:
        django_logout(request)
        # by default, we would like to give him an opportunity to log in again
        return redirect('users:login')
    # This shouldn't really be used, but in case somebody logs out without being logged in prior - goes to index
    return redirect('expense_tracker_app:index')
