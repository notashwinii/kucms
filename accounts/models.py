from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

# Custom User Manager for handling users
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        now = timezone.now()
        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with admin privileges
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Custom User model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLES)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Set only for admin and faculty
    is_superuser = models.BooleanField(default=False)  # Only Admin should have this
    date_joined = models.DateTimeField(auto_now_add=True)
    program = models.ForeignKey('Program', null=True, blank=True, on_delete=models.SET_NULL)  # For students
    department = models.ForeignKey('Department', null=True, blank=True, on_delete=models.SET_NULL)  # For faculty
    session = models.CharField(max_length=10, null=True, blank=True)  # For students
    
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# Department model
class Department(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

# Program model
class Program(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, related_name='programs_in', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Faculty model
class Faculty(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, related_name='faculties', on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Course model
class Course(models.Model):
    course_code = models.CharField(max_length=50, null=True, unique=True)
    course_name = models.CharField(max_length=255, null=True)
    department = models.ForeignKey(Department, null=True, related_name="account_courses", on_delete=models.CASCADE)
    program = models.ForeignKey(Program, null=True, related_name="account_courses", on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name

# ProgramCourse model
class ProgramCourse(models.Model):
    program = models.ForeignKey(Program, related_name='program_courses', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='program_courses', on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)

    class Meta:
        unique_together = ['program', 'course', 'semester']

    def __str__(self):
        return f"{self.program.name} - {self.course.name} ({self.semester})"

# CourseSession model
class CourseSession(models.Model):
    program_course = models.ForeignKey(ProgramCourse, related_name='sessions', on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, related_name='sessions', on_delete=models.CASCADE)
    session_year = models.IntegerField()
    semester = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = ['program_course', 'session_year', 'semester']

    def __str__(self):
        return f"{self.program_course.course.name} - {self.faculty.name} - {self.session_year} - {self.semester}"
