from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet
from . import views


router = DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
path('course/api/course/<str:course_code>/id/', views.get_course_id_by_code, name='get_course_id_by_code'),
    path('api/course/<str:course_id>/notes/', views.get_course_notes, name='get_course_notes'),
    path('api/course/<str:course_id>/upload-note/', views.upload_note, name='upload_note'),
]
