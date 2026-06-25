from django.db import models
from accounts.models import BaseModel


class Department(BaseModel):

    name = models.CharField(
        max_length=255,
        unique=True
    )

    code = models.CharField(
        max_length=20,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
    
class Program(BaseModel):

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="programs"
    )

    name = models.CharField(
        max_length=255
    )

    code = models.CharField(
        max_length=20,
        unique=True
    )

    duration_years = models.PositiveIntegerField(
        default=4
    )

    total_semesters = models.PositiveIntegerField(
        default=8
    )

    def __str__(self):
        return self.name
    
class Semester(BaseModel):

    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name="semesters"
    )

    semester_no = models.PositiveIntegerField()

    title = models.CharField(
        max_length=100
    )

    is_current = models.BooleanField(
        default=False
    )

    class Meta:
        unique_together = (
            "program",
            "semester_no"
        )

    def __str__(self):
        return (
            f"{self.program.name}"
            f" - Semester {self.semester_no}"
        )
    
class Course(BaseModel):

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="courses"
    )

    course_code = models.CharField(
        max_length=20,
        unique=True
    )

    course_title = models.CharField(
        max_length=255
    )

    credit_hours = models.PositiveIntegerField()

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.course_code
    
class SemesterCourse(BaseModel):

    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (
            "semester",
            "course"
        )

class TeacherCourseAssignment(
    BaseModel
):

    teacher = models.ForeignKey(
        "teachers.Teacher",
        on_delete=models.CASCADE,
        related_name="course_assignments"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE
    )

    session = models.CharField(
        max_length=50
    )

    class Meta:
        unique_together = (
            "teacher",
            "course",
            "semester"
        )

