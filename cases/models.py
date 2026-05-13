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
class FileMovement(models.Model):
    MOVEMENT_STATUS = [
        ('In Transit', 'In Transit'),
        ('Received', 'Received'),
        ('Returned', 'Returned'),
    ]
    
    LOCATIONS = [
        ('Registry', 'Registry'),
        ('Judge Chambers', 'Judge Chambers'),
        ('Magistrate Chambers', 'Magistrate Chambers'),
        ('Typist Office', 'Typist Office'),
        ('Deputy Registrar', 'Deputy Registrar'),
        ('Registrar', 'Registrar'),
        ('Accounts', 'Accounts'),
        ('Advocate', 'Advocate'),
        ('Other', 'Other'),
    ]

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='movements')
    from_location = models.CharField(max_length=100, choices=LOCATIONS)
    to_location = models.CharField(max_length=100, choices=LOCATIONS)
    moved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='moved_by')
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_by')
    purpose = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=MOVEMENT_STATUS, default='In Transit')
    moved_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.case.case_number} - {self.from_location} to {self.to_location}"
