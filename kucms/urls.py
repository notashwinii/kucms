from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt import views as jwt_views

# Define the schema view for Swagger UI
schema_view = get_schema_view(
    openapi.Info(
        title="KUCMS API",
        default_version="v1",
        description="API documentation for the classroom management system",
       
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
     path('course/', include('course.urls')), 
    path('accounts/', include('accounts.urls')),  # Make sure you have URL patterns in the accounts app
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI
]
