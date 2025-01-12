from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Department, Faculty, Course, Program, ProgramCourse, CourseSession

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'role', 'is_active', 'is_staff', 'is_superuser', 'date_joined']  # Added is_superuser

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['email'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return user

class DepartmentSerializer(serializers.ModelSerializer):
    # Include programs and faculty members in the department serializer
    programs = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all(), many=True)
    faculties = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all(), many=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'programs', 'faculties']

class ProgramSerializer(serializers.ModelSerializer):
    # Serialize the program under the department context
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

    class Meta:
        model = Program
        fields = ['id', 'name', 'department']

class FacultySerializer(serializers.ModelSerializer):
    # Include courses taught by this faculty
    courses = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True)

    class Meta:
        model = Faculty
        fields = ['id', 'name', 'department', 'description', 'courses']

class CourseSerializer(serializers.ModelSerializer):
    # Include program and faculty members in the course serializer
    program = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all())
    faculty_members = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all(), many=True)

    class Meta:
        model = Course
        fields = ['id', 'course_code', 'course_name', 'program', 'faculty_members']

class ProgramCourseSerializer(serializers.ModelSerializer):
    program = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    
    class Meta:
        model = ProgramCourse
        fields = ['id', 'program', 'course', 'semester']

class CourseSessionSerializer(serializers.ModelSerializer):
    program_course = serializers.PrimaryKeyRelatedField(queryset=ProgramCourse.objects.all())
    faculty = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all())

    class Meta:
        model = CourseSession
        fields = ['id', 'program_course', 'faculty', 'session_year', 'semester', 'start_date', 'end_date']
