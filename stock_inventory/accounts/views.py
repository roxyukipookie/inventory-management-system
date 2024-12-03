# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from .models import UserProfile

# Registration view
def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Check role and set is_active for Owner
            if user.role == 'Owner':
                user.is_active = False  # Owner must be activated by admin
                user.save()
                messages.success(request, 'Registration successful. Please wait for admin verification.')
                return redirect('login')  # Redirect to login after successful registration
            else:
                messages.success(request, 'Registration successful! You can log in now.')
                return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please try again.')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/signup.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('dashboard_view')  # Redirect to dashboard after successful login
            else:
                messages.error(request, 'Your account is not active. Please wait for admin verification.')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')


def redirect_to_login(request):
    if request.user.is_authenticated:
        return redirect('login')  # Redirect to dashboard if logged in
    else:
        return redirect('login')  # Otherwise, redirect to login page
    

def get_user_role(user):
    try:
        user_profile = UserProfile.objects.get(user=user)
        return 'staff' if user_profile.owner else 'owner'
    except UserProfile.DoesNotExist:
        return 'owner'  # Default to owner if no UserProfile is set up