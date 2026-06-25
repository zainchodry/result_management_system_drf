from django.db import models

from accounts.models import BaseModel


class Teacher(BaseModel):

    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    )

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="teacher"
    )

    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.PROTECT
    )

    employee_id = models.CharField(
        max_length=50,
        unique=True
    )

    designation = models.CharField(
        max_length=100
    )

    joining_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    def __str__(self):
        return self.employee_id

class TeacherQualification(BaseModel):

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="qualifications"
    )

    degree = models.CharField(
        max_length=255
    )

    institute = models.CharField(
        max_length=255
    )

    year = models.IntegerField()

class TeacherDocument(BaseModel):

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    title = models.CharField(
        max_length=255
    )

    file = models.FileField(
        upload_to="teacher_documents/"
    )

