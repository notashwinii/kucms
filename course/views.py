from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer


from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Note, Course
from .serializers import NoteSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

def get_course_id_by_code(request, course_code):
    course = get_object_or_404(Course, course_code=course_code)  # Adjust if needed
    return JsonResponse({'course_id': course.id})

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_course_notes(request, course_id):
    course = Course.objects.get(id=course_id)

    # Check if the user is enrolled or a faculty member in the course
    if request.user not in course.faculty_members.all() and not request.user.is_staff:
        return Response(
            {"detail": "You do not have permission to view these notes."},
            status=status.HTTP_403_FORBIDDEN,
        )

    notes = course.notes.all()
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_note(request, course_id):
    course = Course.objects.get(id=course_id)

    # Check if the user is a faculty member
    if not request.user.is_staff:
        return Response(
            {"detail": "Only faculty can upload notes."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "POST":
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course, uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Action to get all notes of a specific course
    @action(detail=True, methods=["get"])
    def notes(self, request, pk=None):
        course = self.get_object()
        notes = Note.objects.filter(course=course)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
