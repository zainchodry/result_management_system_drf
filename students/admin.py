from django.contrib import admin

from .models import (
    Student,
    StudentSemesterHistory,
    StudentDocument
)

admin.site.register(Student)
admin.site.register(StudentSemesterHistory)
admin.site.register(StudentDocument)