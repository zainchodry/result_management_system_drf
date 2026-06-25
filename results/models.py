from django.db import models

from accounts.models import BaseModel

class GradeScale(BaseModel):

    min_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    max_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    grade = models.CharField(
        max_length=5
    )

    grade_points = models.DecimalField(
        max_digits=3,
        decimal_places=2
    )

    class Meta:
        ordering = ["-min_percentage"]

    def __str__(self):
        return self.grade
    
class SemesterResult(BaseModel):

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="semester_results"
    )

    semester = models.ForeignKey(
        "academics.Semester",
        on_delete=models.CASCADE
    )

    gpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.00
    )

    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.00
    )

    total_credit_hours = models.PositiveIntegerField(
        default=0
    )

    earned_credit_hours = models.PositiveIntegerField(
        default=0
    )

    is_published = models.BooleanField(
        default=False
    )

    is_locked = models.BooleanField(
        default=False
    )

    class Meta:
        unique_together = (
            "student",
            "semester"
        )

class ResultItem(BaseModel):

    semester_result = models.ForeignKey(
        SemesterResult,
        on_delete=models.CASCADE,
        related_name="subjects"
    )

    course = models.ForeignKey(
        "academics.Course",
        on_delete=models.CASCADE
    )

    teacher = models.ForeignKey(
        "teachers.Teacher",
        on_delete=models.SET_NULL,
        null=True
    )

    total_marks = models.PositiveIntegerField()

    obtained_marks = models.PositiveIntegerField()

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    grade = models.CharField(
        max_length=5
    )

    grade_points = models.DecimalField(
        max_digits=3,
        decimal_places=2
    )

    is_passed = models.BooleanField(
        default=True
    )

class ResultPublication(BaseModel):

    semester = models.ForeignKey(
        "academics.Semester",
        on_delete=models.CASCADE
    )

    published_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True
    )

    published_at = models.DateTimeField(
        auto_now_add=True
    )

