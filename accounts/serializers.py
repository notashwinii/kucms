from rest_framework import serializers
from .models import CustomUser, Department, Faculty, Course, Program

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'role', 'is_active', 'is_staff', 'date_joined']  # Updated fields

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
    
    program = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all())
    faculty_members = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all(), many=True)

    class Meta:
        model = Course
        fields = ['id', 'course_code', 'course_name', 'program', 'faculty_members']
        ref_name = 'AccountCourseSerializer' 
