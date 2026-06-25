from django.db import models

from accounts.models import BaseModel


class Student(BaseModel):

    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("GRADUATED", "Graduated"),
        ("SUSPENDED", "Suspended"),
        ("DROPPED", "Dropped"),
    )

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="student"
    )

    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.PROTECT
    )

    program = models.ForeignKey(
        "academics.Program",
        on_delete=models.PROTECT
    )

    current_semester = models.ForeignKey(
        "academics.Semester",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    roll_number = models.CharField(
        max_length=50,
        unique=True
    )

    registration_number = models.CharField(
        max_length=50,
        unique=True
    )

    admission_year = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    cgpa = models.DecimalField(  # Added: was missing but referenced in results/views.py
        max_digits=4,
        decimal_places=2,
        default=0.00
    )

    guardian_name = models.CharField(max_length=255)

    guardian_phone = models.CharField(max_length=20)

    emergency_contact = models.CharField(max_length=20)

    def __str__(self):
        return self.roll_number


class StudentSemesterHistory(BaseModel):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="semester_history"
    )

    semester = models.ForeignKey(
        "academics.Semester",
        on_delete=models.CASCADE
    )

    promoted_date = models.DateField()

    class Meta:
        ordering = ["semester__semester_no"]


class StudentDocument(BaseModel):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    title = models.CharField(max_length=255)

    file = models.FileField(upload_to="student_documents/")
