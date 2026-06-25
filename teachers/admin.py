from django.contrib import admin
from .models import Teacher, TeacherQualification, TeacherDocument


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'get_full_name', 'department', 'designation', 'status', 'joining_date')
    list_filter = ('status', 'department')
    search_fields = ('employee_id', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('employee_id', 'created_at', 'updated_at')

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'


@admin.register(TeacherQualification)
class TeacherQualificationAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'degree', 'institute', 'year')
    search_fields = ('teacher__employee_id', 'degree', 'institute')
    ordering = ('-year',)


@admin.register(TeacherDocument)
class TeacherDocumentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'title', 'created_at')
    search_fields = ('teacher__employee_id', 'title')