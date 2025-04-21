from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from accounts.forms import UserLoginForm, UserRegistrationForm
from accounts.models import User


def user_login(request):
    """
    Handle user login process.

    Authenticates the user using email and password, and redirects to home on success.
    Displays appropriate error messages on failure.
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, email=data['email'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.', extra_tags='success')
                return redirect('shop:home')
            else:
                messages.error(request, 'Email or password is incorrect.', extra_tags='danger')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    """
    Log the user out and redirect to the home page.
    """
    logout(request)
    messages.success(request, 'Logout successful.', extra_tags='success')
    return redirect('shop:home')


def register(request):
    """
    Handle user registration process.

    Creates a new user account, logs the user in, and redirects to home on success.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['email'],
                data['full_name'],
                data['phone_number'],
                data['password']
            )
            login(request, user)
            messages.success(request, 'You have registered successfully.', extra_tags='success')
            return redirect('shop:home')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})
