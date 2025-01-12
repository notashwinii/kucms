from django.contrib import admin
from .models import CustomUser, Department, Program, Faculty, Course, ProgramCourse

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'role', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['email', 'role']
    list_filter = ['role', 'is_active', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(Program)

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'description')
    search_fields = ('name', 'department__name')

admin.site.register(Faculty, FacultyAdmin)

class ProgramCourseInline(admin.TabularInline):
    model = ProgramCourse
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'department', 'program')
    search_fields = ('course_code', 'course_name')
    list_filter = ('department', 'program')
    inlines = [ProgramCourseInline]

admin.site.register(Course, CourseAdmin)
