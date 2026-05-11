from django.contrib import admin
from .models import Case, Document, Hearing, Party

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['case_number', 'case_title', 'date_filed', 'case_status', 'assigned_to']
    search_fields = ['case_number', 'case_title', 'parties']
    list_filter = ['case_status']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'case', 'document_type', 'is_verified', 'uploaded_at', 'uploaded_by']
    search_fields = ['title', 'case__case_number']
    list_filter = ['document_type', 'is_verified']

@admin.register(Hearing)
class HearingAdmin(admin.ModelAdmin):
    list_display = ['case', 'hearing_date', 'purpose', 'outcome']
    search_fields = ['case__case_number', 'purpose']
    list_filter = ['hearing_date']

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ['name', 'case', 'role']
    search_fields = ['name', 'case__case_number']
    list_filter = ['role']