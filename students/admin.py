from django.contrib import admin
from .models import Student, StudentSemesterHistory, StudentDocument


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'get_full_name', 'program', 'department', 'status', 'cgpa', 'admission_year')
    list_filter = ('status', 'program', 'department', 'admission_year')
    search_fields = ('roll_number', 'registration_number', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('roll_number', 'registration_number', 'cgpa', 'created_at', 'updated_at')

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'


@admin.register(StudentSemesterHistory)
class StudentSemesterHistoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'promoted_date')
    list_filter = ('semester',)
    search_fields = ('student__roll_number',)


@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'created_at')
    search_fields = ('student__roll_number', 'title')