from django.db import models
from accounts.models import Department, Program, Faculty
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.conf import settings



class Course(models.Model):
    course_code = models.CharField(max_length=50, null=True, unique=True)
    course_name = models.CharField(max_length=255, null=True)
    department = models.ForeignKey(Department, null=True, related_name="course_courses", on_delete=models.CASCADE)
    program = models.ForeignKey(Program, null=True, related_name="course_courses", on_delete=models.CASCADE)
    faculty_members = models.ManyToManyField(Faculty, related_name="course_courses")

    def __str__(self):
        return self.course_name


class Note(models.Model):
    course = models.ForeignKey(Course, related_name='notes', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.FileField(upload_to='notes/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
