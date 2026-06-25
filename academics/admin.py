from django.contrib import admin
from .models import Department, Program, Semester, Course, SemesterCourse, TeacherCourseAssignment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'duration_years', 'total_semesters')
    list_filter = ('department',)
    search_fields = ('name', 'code')


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'semester_no', 'is_current')
    list_filter = ('program', 'is_current')
    search_fields = ('title',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_title', 'department', 'credit_hours')
    list_filter = ('department',)
    search_fields = ('course_code', 'course_title')


@admin.register(SemesterCourse)
class SemesterCourseAdmin(admin.ModelAdmin):
    list_display = ('semester', 'course')
    list_filter = ('semester',)


@admin.register(TeacherCourseAssignment)
class TeacherCourseAssignmentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'course', 'semester', 'session')
    list_filter = ('semester', 'session')
    search_fields = ('teacher__employee_id', 'course__course_code')