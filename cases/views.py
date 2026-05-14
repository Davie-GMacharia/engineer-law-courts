from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        country_code = request.POST.get('country_code')
        phone_number = request.POST.get('phone_number')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered!')
            return render(request, 'register.html')

        full_phone = f"{country_code}{phone_number.lstrip('0')}"

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=False
        )

        UserProfile.objects.create(
            user=user,
            role=role,
            phone_number=full_phone,
            is_approved=False
        )

        messages.success(request, 'Account created! Please wait for admin approval.')
        return redirect('login')

    return render(request, 'register.html')

# ================== UPDATED REGISTER FUNCTION ==================
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        country_code = request.POST.get('country_code')
        phone_number = request.POST.get('phone_number')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered!')
            return render(request, 'register.html')

        full_phone = f"{country_code}{phone_number.lstrip('0')}"

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=False
        )

        UserProfile.objects.create(
            user=user,
            role=role,
            phone_number=full_phone,
            is_approved=False
        )

        messages.success(request, 'Account created successfully! Please wait for admin approval.')
        return redirect('login')

    return render(request, 'register.html')
