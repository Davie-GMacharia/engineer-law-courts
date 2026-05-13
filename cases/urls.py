from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('pending-users/', views.pending_users, name='pending_users'),
    path('approve-user/<int:user_id>/', views.approve_user, name='approve_user'),

    # Cases
    path('cases/', views.cases_list, name='cases_list'),
    path('cases/new/', views.case_new, name='case_new'),
    path('cases/<int:pk>/', views.case_detail, name='case_detail'),

    # Documents
    path('documents/', views.documents_list, name='documents_list'),
    path('cases/<int:case_pk>/documents/upload/', views.document_upload, name='document_upload'),

    # Hearings
    path('hearings/', views.hearings_list, name='hearings_list'),
    path('cases/<int:case_pk>/hearings/new/', views.hearing_new, name='hearing_new'),

    # File Movements
    path('movements/', views.file_movements_list, name='file_movements_list'),
    path('cases/<int:case_pk>/movements/new/', views.file_movement_new, name='file_movement_new'),
    path('movements/<int:movement_pk>/receive/', views.file_movement_receive, name='file_movement_receive'),
]
