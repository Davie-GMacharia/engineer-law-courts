from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Case, Document, Hearing, Party, UserProfile, FileMovement

# ================== AUTH ==================
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

        full_phone = f"{country_code}{phone_number.lstrip('0')}" if country_code and phone_number else phone_number

        try:
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
        except Exception as e:
            messages.error(request, 'Error creating account. Please try again.')
            return render(request, 'register.html')

    return render(request, 'register.html')


# ================== CORE VIEWS ==================
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {})


@login_required
def pending_users(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission.")
        return redirect('dashboard')
    
    pending = UserProfile.objects.filter(is_approved=False).select_related('user').order_by('-user__date_joined')
    return render(request, 'pending_users.html', {'pending': pending})


@login_required
def approve_user(request, user_id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission.")
        return redirect('dashboard')
    
    profile = get_object_or_404(UserProfile, user_id=user_id)
    profile.is_approved = True
    profile.user.is_active = True
    profile.user.save()
    profile.save()
    messages.success(request, f'{profile.user.email} approved successfully.')
    return redirect('pending_users')


# ================== PLACEHOLDER VIEWS (to satisfy urls.py) ==================
@login_required
def cases_list(request):
    cases = Case.objects.all().order_by('-created_at')
    return render(request, 'cases_list.html', {'cases': cases})

@login_required
def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    return render(request, 'case_detail.html', {'case': case})

@login_required
def documents_list(request):
    return render(request, 'documents_list.html', {})

@login_required
def case_new(request):
    return render(request, 'case_new.html', {})

@login_required
def file_movements_list(request):
    movements = FileMovement.objects.all().order_by('-movement_date')
    return render(request, 'file_movements_list.html', {'movements': movements})

@login_required
def document_upload(request, case_pk):
    return redirect('case_detail', pk=case_pk)

@login_required
def hearing_new(request, case_pk):
    return redirect('case_detail', pk=case_pk)

@login_required
def file_movement_new(request, case_pk):
    return redirect('case_detail', pk=case_pk)

@login_required
def file_movement_receive(request, movement_pk):
    return redirect('file_movements_list')
