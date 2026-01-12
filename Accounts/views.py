from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .models import MyUser
from django.contrib import messages
# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

import random

def generate_otp():
    return str(random.randint(100000, 999999))

def auth(request):
    """Handles Login: Phone + Password with Admin Check"""
    next_url = request.GET.get('next') or request.POST.get('next') or 'index'

    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        try:
            # 1. Fetch user by phone to get the internal username
            user_obj = MyUser.objects.get(phone=phone)
            
            # 2. Authenticate using the username (as required by Django internals)
            user = authenticate(request, username=user_obj.username, password=password)
            
            if user is not None:
                login(request, user)
                
                # 3. Check for is_admin status
                if user.is_admin:
                    # Render the specific admin template
                    return redirect('Admin_dashboard')
                
                # Standard user redirect
                return redirect(next_url)
            else:
                messages.error(request, "Incorrect password.")
        
        except MyUser.DoesNotExist:
            messages.error(request, "Phone number not registered.")

    return render(request, 'Auth/auth.html', {'next': next_url})


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'Auth/auth.html')

        if MyUser.objects.filter(phone=phone).exists():
            messages.error(request, "This phone number is already registered.")
            return render(request, 'Auth/auth.html')

        try:
            # We create the instance manually to avoid the Manager passing 'email'
            user = MyUser(
                username=phone,
                phone=phone,
                name=name
            )
            user.set_password(password) # This hashes the password correctly
            user.save() # This triggers your generate_server_id() logic
            
            login(request, user)
            messages.success(request, f"Welcome {name}! Your ID is {user.server_id}")
            return redirect('index')
            
        except Exception as e:
            print(f"Registration Error: {e}")
            messages.error(request, "An error occurred during registration.")
            return render(request, 'Auth/auth.html')
    return render(request, 'Auth/auth.html')
def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to home page after logout