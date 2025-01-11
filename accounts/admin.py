from django.contrib import admin
from .models import CustomUser,Department, Program, Faculty, Course

# Register your models here

admin.site.register(CustomUser)
admin.site.register(Department)
admin.site.register(Program)
admin.site.register(Faculty)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'department', 'program')
    search_fields = ('course_code', 'course_name')

admin.site.register(Course, CourseAdmin)
