from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.contrib import messages
from django import forms

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Check if username already exists
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken. Please choose a different one.')
                print("Username already taken.")  # Debug message
            else:
                user = form.save()
                login(request, user)
                print("User registered and logged in. Redirecting to dashboard...")  # Debug message
                return redirect('dashboard_view')  # Redirect to dashboard
        else:
            print("Form is not valid. Errors:", form.errors)  # Debug message
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password1')

        try:
            # Get the user with the provided email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        
        if user:
            # Use the username for authentication (User object will have username)
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard_view')
            else:
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'Email not found')
    
    return render(request, 'accounts/login.html')

