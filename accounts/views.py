from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import login

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
