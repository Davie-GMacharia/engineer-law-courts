from django import forms
from .models import Case, Document

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['case_number', 'case_title', 'parties', 'date_filed', 'case_status', 'assigned_to']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['case', 'document_type', 'title', 'file', 'notes']