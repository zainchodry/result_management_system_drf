from django.contrib import admin
from .models import GradeScale, SemesterResult, ResultItem, ResultPublication


@admin.register(GradeScale)
class GradeScaleAdmin(admin.ModelAdmin):
    list_display = ('grade', 'min_percentage', 'max_percentage', 'grade_points')
    ordering = ('-min_percentage',)


@admin.register(SemesterResult)
class SemesterResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'gpa', 'cgpa', 'is_published', 'is_locked', 'created_at')
    list_filter = ('is_published', 'is_locked', 'semester')
    search_fields = ('student__roll_number', 'student__user__email')
    ordering = ('-created_at',)
    readonly_fields = ('gpa', 'cgpa', 'created_at', 'updated_at')
    actions = ['publish_results', 'lock_results']

    def publish_results(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, "Selected results have been published.")
    publish_results.short_description = "Publish selected results"

    def lock_results(self, request, queryset):
        queryset.update(is_locked=True)
        self.message_user(request, "Selected results have been locked.")
    lock_results.short_description = "Lock selected results"


@admin.register(ResultItem)
class ResultItemAdmin(admin.ModelAdmin):
    list_display = ('get_student', 'course', 'obtained_marks', 'total_marks', 'percentage', 'grade', 'is_passed')
    list_filter = ('is_passed', 'grade', 'course')
    search_fields = ('semester_result__student__roll_number', 'course__course_code')
    readonly_fields = ('percentage', 'grade', 'grade_points', 'is_passed')

    def get_student(self, obj):
        return obj.semester_result.student.roll_number
    get_student.short_description = 'Roll Number'


@admin.register(ResultPublication)
class ResultPublicationAdmin(admin.ModelAdmin):
    list_display = ('semester', 'published_by', 'published_at')
    readonly_fields = ('published_at',)
