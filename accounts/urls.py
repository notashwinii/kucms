from django.urls import path
from .views import DepartmentView, FacultyView, CourseView, ProgramView, UserDetailView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='user-login'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('departments/', DepartmentView.as_view(), name='department-list'),
    path('faculties/', FacultyView.as_view(), name='faculty-list'),
    path('courses/', CourseView.as_view(), name='course-list'),
    path('programs/', ProgramView.as_view(), name='program-list'),
]
