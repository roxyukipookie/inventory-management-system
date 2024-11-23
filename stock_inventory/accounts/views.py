from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, Role
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                # Save the user and return the instance
                user = form.save()
                
                # Log the user in after successful registration
                login(request, user)
                return redirect('dashboard_view')
            except Exception as e:
                messages.error(request, f"Error creating account: {e}")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

@login_required
def staff_list(request):
    staff_users = CustomUser.objects.filter(role__name='staff')
    return render(request, 'accounts/staff_list.html', {'staff_users': staff_users})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user using email and password
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_view')
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, 'accounts/login.html')
