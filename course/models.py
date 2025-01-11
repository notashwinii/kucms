from django.db import models
from accounts.models import Department, Program, Faculty

class Course(models.Model):
    course_code = models.CharField(max_length=50, null=True, unique=True)
    course_name = models.CharField(max_length=255, null=True)
    department = models.ForeignKey(Department, null=True, related_name="course_courses", on_delete=models.CASCADE)
    program = models.ForeignKey(Program, null=True, related_name="course_courses", on_delete=models.CASCADE)
    faculty_members = models.ManyToManyField(Faculty, related_name="course_courses")

    def __str__(self):
        return self.course_name
