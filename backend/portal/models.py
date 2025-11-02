from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Program(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Student(models.Model):
    COMMUNITY_CHOICES = [
        ('General', 'General'),
        ('OBC', 'OBC'),
        ('SC', 'SC'),
        ('ST', 'ST'),
    ]

    PAYMENT_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
    ]

    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
    ]

    application_no = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    community = models.CharField(max_length=20, choices=COMMUNITY_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='Pending')
    admission_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')
    counsellor = models.ForeignKey('Counsellor', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.application_no} - {self.name}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.attendance_percentage}%"

class AssignmentMark(models.Model):
    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Pending', 'Pending'),
        ('Graded', 'Graded'),
    ]

    reg_no = models.CharField(max_length=20, unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    p_code = models.CharField(max_length=20)  # Paper code
    internal_marks = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reg_no} - {self.p_code} - {self.internal_marks}"

class Counsellor(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    counsellor_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    aadhaar_card = models.CharField(max_length=12, unique=True)
    qualification = models.CharField(max_length=100)
    highest_qualification = models.CharField(max_length=100)
    programme_assigned = models.ForeignKey(Program, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=10)
    alternate_number = models.CharField(max_length=10, blank=True)
    email_id = models.EmailField(unique=True)
    current_designation = models.CharField(max_length=100)
    working_experience = models.TextField()
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    address_line3 = models.CharField(max_length=255, blank=True)
    pincode = models.CharField(max_length=6)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.counsellor_name