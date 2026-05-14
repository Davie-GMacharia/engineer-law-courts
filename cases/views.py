from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Case, Document, Hearing, Party, UserProfile

# ================== MAIN VIEWS ==================
@login_required
def dashboard(request):
    now = timezone.now()
    context = {
        'total_cases': Case.objects.count(),
        'active_cases': Case.objects.filter(case_status='Active').count(),
        'total_documents': Document.objects.count(),
        'upcoming_hearings': Hearing.objects.filter(hearing_date__gte=now).count(),
        'recent_cases': Case.objects.order_by('-created_at')[:6],
    }
    return render(request, 'dashboard.html', context)


@login_required
def cases_list(request):
    cases = Case.objects.all().order_by('-created_at')
    return render(request, 'cases_list.html', {'cases': cases})


# ================== IMPROVED REGISTER VIEW ==================
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

        full_phone = f"{country_code}{phone_number.lstrip('0')}" if country_code else phone_number

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
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'register.html')

    return render(request, 'register.html')


# Add other missing views as placeholders to prevent errors
@login_required
def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    return render(request, 'case_detail.html', {'case': case})


@login_required
def pending_users(request):
    pending = UserProfile.objects.filter(is_approved=False).select_related('user')
    return render(request, 'pending_users.html', {'pending': pending})
