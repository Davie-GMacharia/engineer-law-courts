from django.db import models
from django.contrib.auth.models import User

class Case(models.Model):
    case_number = models.CharField(max_length=50, unique=True)
    case_title = models.CharField(max_length=300)
    parties = models.TextField()
    date_filed = models.DateField()
    case_status = models.CharField(max_length=20, choices=[
        ('Active', 'Active'),
        ('Closed', 'Closed'),
        ('Appealed', 'Appealed')
    ], default='Active')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.case_number


class Document(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=100, choices=[
        ('Pleading', 'Pleading'),
        ('Judgment', 'Judgment'),
        ('Evidence', 'Evidence'),
        ('Affidavit', 'Affidavit'),
        ('Order', 'Order'),
        ('Other', 'Other')
    ])
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='court_documents/%Y/%m/%d/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.case.case_number}"
class Hearing(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='hearings')
    hearing_date = models.DateTimeField()
    purpose = models.CharField(max_length=200)
    outcome = models.TextField(blank=True)
class Party(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='party_set')
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=20, choices=[('Plaintiff','Plaintiff'),('Defendant','Defendant')])