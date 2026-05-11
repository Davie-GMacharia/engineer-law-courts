
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/cases', views.CaseViewSet)
router.register(r'api/documents', views.DocumentViewSet)
router.register(r'api/hearings', views.HearingViewSet)
router.register(r'api/parties', views.PartyViewSet)

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', 
auth_views.LoginView.as_view(template_name='login.html'), 
name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), 
name='logout'),

    # Cases
    path('cases/', views.cases_list, name='cases_list'),
    path('cases/new/', views.case_new, name='case_new'),
    path('cases/<int:pk>/', views.case_detail, name='case_detail'),

    # Documents
    path('documents/', views.documents_list, name='documents_list'),
    path('cases/<int:case_pk>/documents/upload/', 
views.document_upload, name='document_upload'),

    # Hearings
    path('hearings/', views.hearings_list, name='hearings_list'),
    path('cases/<int:case_pk>/hearings/new/', views.hearing_new, 
name='hearing_new'),
] + router.urls
