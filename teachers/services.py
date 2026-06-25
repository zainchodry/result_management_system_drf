from datetime import datetime
from django.contrib.auth import get_user_model

from accounts.utils import (
    generate_temporary_password
)

from accounts.tasks import (
    send_account_credentials_email
)

from .models import Teacher

User = get_user_model()

def generate_employee_id(count):

    year = datetime.now().year

    return f"EMP-{year}-{count:04d}"

def create_teacher(validated_data):

    temp_password = (
        generate_temporary_password()
    )

    email = validated_data["email"]

    user = User.objects.create_user(
        username=email,
        email=email,
        password=temp_password,
        role="TEACHER",
        first_name=validated_data["first_name"],
        last_name=validated_data["last_name"],
        must_change_password=True
    )

    teacher_count = (
        Teacher.objects.count() + 1
    )

    teacher = Teacher.objects.create(
        user=user,
        department_id=validated_data[
            "department_id"
        ],
        employee_id=generate_employee_id(
            teacher_count
        ),
        designation=validated_data[
            "designation"
        ],
        joining_date=validated_data[
            "joining_date"
        ]
    )

    send_account_credentials_email.delay(
        email,
        temp_password,
        "Teacher"
    )

    return teacher
