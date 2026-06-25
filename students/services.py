from datetime import datetime
from django.contrib.auth import get_user_model

from accounts.utils import (
    generate_temporary_password
)

from accounts.tasks import (
    send_account_credentials_email
)

from .models import Student

User = get_user_model()

def generate_roll_number(program_code, count):
    year = datetime.now().year

    return f"FA{str(year)[2:]}-{program_code}-{count:03d}"


def create_student(
    validated_data
):

    temp_password = (
        generate_temporary_password()
    )

    email = validated_data["email"]

    user = User.objects.create_user(
        username=email,
        email=email,
        password=temp_password,
        role="STUDENT",
        first_name=validated_data[
            "first_name"
        ],
        last_name=validated_data[
            "last_name"
        ],
        must_change_password=True
    )

    student = Student.objects.create(
        user=user,
        department_id=validated_data[
            "department_id"
        ],
        program_id=validated_data[
            "program_id"
        ],
        guardian_name=validated_data[
            "guardian_name"
        ],
        guardian_phone=validated_data[
            "guardian_phone"
        ],
        emergency_contact=validated_data[
            "emergency_contact"
        ],
        roll_number="TEMP",
        registration_number="TEMP",
        admission_year=2026
    )

    send_account_credentials_email.delay(
        email,
        temp_password,
        "Student"
    )

    return student

