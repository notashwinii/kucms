from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLES)
    department = models.ForeignKey(
        'Department', on_delete=models.SET_NULL, null=True, blank=True
    )

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

class Course(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    session = models.CharField(max_length=20)
