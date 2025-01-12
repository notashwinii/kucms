from rest_framework import serializers
from .models import Course
from accounts.models import Faculty, Department, Program
from .models import Note


class CourseSerializer(serializers.ModelSerializer):
    faculty_members = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), many=True
    )
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    program = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all())

    class Meta:
        model = Course
        fields = [
            "id",
            "course_code",
            "course_name",
            "department",
            "program",
            "faculty_members",
        ]
        ref_name = "CourseCourseSerializer"


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "description", "file", "uploaded_by", "uploaded_at"]
