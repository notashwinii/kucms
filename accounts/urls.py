from django.urls import path
from .views import LoginView, UserDetailView, DepartmentView, ProgramView, FacultyView, CourseView, RegisterUserView

urlpatterns = [
    # Authentication views
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user_detail'),

    # Admin management views
    path('departments/', DepartmentView.as_view(), name='department_list'),
    path('programs/', ProgramView.as_view(), name='program_list'),
    path('faculties/', FacultyView.as_view(), name='faculty_list'),
    path('courses/', CourseView.as_view(), name='course_list'),

    # User registration
    path('register/', RegisterUserView.as_view(), name='register_user'),
]
