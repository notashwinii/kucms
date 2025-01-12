from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import CustomUser, Department, Faculty, Course, Program
from .serializers import UserSerializer, LoginSerializer, DepartmentSerializer, FacultySerializer, CourseSerializer, ProgramSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


# --- Login Views ---
class LoginView(APIView):
    @swagger_auto_schema(
        operation_summary="User Login",
        operation_description="Authenticate the user and return JWT access and refresh tokens.",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING, description="JWT refresh token"),
                        "access": openapi.Schema(type=openapi.TYPE_STRING, description="JWT access token"),
                    },
                ),
            ),
            400: "Invalid credentials or bad request",
        },
    )
    def post(self, request):
        """
        Authenticate user and return JWT tokens.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="User Details",
        operation_description="Retrieve details of the currently authenticated user.",
        responses={
            200: openapi.Response(
                description="User details",
                schema=UserSerializer,
            ),
            401: "Unauthorized - Authentication credentials were not provided.",
        },
    )
    def get(self, request):
        """
        Retrieve details of the currently authenticated user.
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


# --- Admin Management Views ---
class DepartmentView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="List Departments",
        operation_description="Retrieve a list of all departments.",
        responses={
            200: DepartmentSerializer(many=True),
        },
    )
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create Department",
        operation_description="Add a new department.",
        request_body=DepartmentSerializer,
        responses={
            201: DepartmentSerializer,
            400: "Bad request - Invalid data",
        },
    )
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProgramView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="List Programs",
        operation_description="Retrieve a list of all programs.",
        responses={
            200: ProgramSerializer(many=True),
        },
    )
    def get(self, request):
        programs = Program.objects.all()
        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create Program",
        operation_description="Add a new program under a department.",
        request_body=ProgramSerializer,
        responses={
            201: ProgramSerializer,
            400: "Bad request - Invalid data",
        },
    )
    def post(self, request):
        serializer = ProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FacultyView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="List Faculties",
        operation_description="Retrieve a list of all faculties.",
        responses={
            200: FacultySerializer(many=True),
        },
    )
    def get(self, request):
        faculties = Faculty.objects.all()
        serializer = FacultySerializer(faculties, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create Faculty",
        operation_description="Add a new faculty.",
        request_body=FacultySerializer,
        responses={
            201: FacultySerializer,
            400: "Bad request - Invalid data",
        },
    )
    def post(self, request):
        serializer = FacultySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="List Courses",
        operation_description="Retrieve a list of all courses.",
        responses={
            200: CourseSerializer(many=True),
        },
    )
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create Course",
        operation_description="Add a new course under a program and faculty.",
        request_body=CourseSerializer,
        responses={
            201: CourseSerializer,
            400: "Bad request - Invalid data",
        },
    )
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- User Registration Views ---
class RegisterUserView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Register New User",
        operation_description="Register a new user (admin, faculty, or student).",
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            400: "Bad request - Invalid data",
        },
    )
    def post(self, request):
        """
        Register a new user with the role (admin, faculty, or student).
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(user, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
