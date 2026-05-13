from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Case, Document, Hearing, Party


@login_required
def dashboard(request):
    now = timezone.now()
    context = {
        'total_cases': Case.objects.count(),
        'active_cases': 
Case.objects.filter(case_status='Active').count(),
        'total_documents': Document.objects.count(),
        'upcoming_hearings': 
Hearing.objects.filter(hearing_date__gte=now, hearing_date__lte=now + 
timedelta(days=30)).count(),
        'recent_cases': Case.objects.order_by('-created_at')[:6],
        'upcoming_hearing_list': 
Hearing.objects.filter(hearing_date__gte=now).order_by('hearing_date')[:5],
    }
    return render(request, 'dashboard.html', context)


@login_required
def cases_list(request):
    cases = Case.objects.all().order_by('-created_at')
    return render(request, 'cases_list.html', {'cases': cases})


@login_required
def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    return render(request, 'case_detail.html', {'case': case})


@login_required
def case_new(request):
    if request.method == 'POST':
        assigned_to_id = request.POST.get('assigned_to')
        case = Case.objects.create(
            case_number=request.POST['case_number'],
            case_title=request.POST['case_title'],
            parties=request.POST['parties'],
            date_filed=request.POST['date_filed'],
            case_status=request.POST.get('case_status', 'Active'),
            assigned_to_id=assigned_to_id if assigned_to_id else None,
        )
        messages.success(request, f'Case {case.case_number} filed successfully.')
        return redirect('case_detail', pk=case.pk)
    users = User.objects.filter(is_active=True)
    return render(request, 'case_new.html', {'users': users})


@login_required
def document_upload(request, case_pk):
    case = get_object_or_404(Case, pk=case_pk)
    if request.method == 'POST':
        Document.objects.create(
            case=case,
            title=request.POST['title'],
            document_type=request.POST['document_type'],
            file=request.FILES['file'],
            notes=request.POST.get('notes', ''),
            uploaded_by=request.user,
        )
        messages.success(request, 'Document uploaded successfully.')
        return redirect('case_detail', pk=case_pk)
    return render(request, 'document_upload.html', {'case': case})


@login_required
def documents_list(request):
    documents = Document.objects.all().order_by('-uploaded_at')
    return render(request, 'documents_list.html', {'documents': 
documents})


@login_required
def hearings_list(request):
    hearings = Hearing.objects.all().order_by('hearing_date')
    return render(request, 'hearings_list.html', {'hearings': 
hearings})


@login_required
def hearing_new(request, case_pk):
    case = get_object_or_404(Case, pk=case_pk)
    if request.method == 'POST':
        Hearing.objects.create(
            case=case,
            hearing_date=request.POST['hearing_date'],
            purpose=request.POST['purpose'],
            outcome=request.POST.get('outcome', ''),
        )
        messages.success(request, 'Hearing scheduled successfully.')
        return redirect('case_detail', pk=case_pk)
    return render(request, 'hearing_new.html', {'case': case})


# API Views
from rest_framework import viewsets
from .serializers import CaseSerializer, DocumentSerializer, HearingSerializer, PartySerializer

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class HearingViewSet(viewsets.ModelViewSet):
    queryset = Hearing.objects.all()
    serializer_class = HearingSerializer

class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
@login_required
def file_movement_new(request, case_pk):
    case = get_object_or_404(Case, pk=case_pk)
    if request.method == 'POST':
        from .models import FileMovement
        FileMovement.objects.create(
            case=case,
            from_location=request.POST['from_location'],
            to_location=request.POST['to_location'],
            moved_by=request.user,
            purpose=request.POST['purpose'],
            status='In Transit',
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'File movement recorded successfully.')
        return redirect('case_detail', pk=case_pk)
    return render(request, 'file_movement_new.html', {'case': case})


@login_required
def file_movement_receive(request, movement_pk):
    from .models import FileMovement
    from django.utils import timezone
    movement = get_object_or_404(FileMovement, pk=movement_pk)
    if request.method == 'POST':
        movement.status = 'Received'
        movement.received_by = request.user
        movement.received_at = timezone.now()
        movement.save()
        messages.success(request, 'File receipt confirmed.')
        return redirect('case_detail', pk=movement.case.pk)
    return render(request, 'file_movement_receive.html', {'movement': movement})


@login_required
def file_movements_list(request):
    from .models import FileMovement
    movements = FileMovement.objects.all().order_by('-moved_at')
    return render(request, 'file_movements_list.html', {'movements': movements})
