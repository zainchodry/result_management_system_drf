from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.utils import generate_temporary_password
from accounts.tasks import send_account_credentials_email
from .models import Student

User = get_user_model()


def generate_roll_number(program_code, admission_year, count):
    """Generate a unique roll number: FA{YY}-{PROGRAM_CODE}-{COUNT:03d}"""
    year_suffix = str(admission_year)[2:]
    return f"FA{year_suffix}-{program_code.upper()}-{count:03d}"


def generate_registration_number(program_code, admission_year, count):
    """Generate a unique registration number."""
    return f"REG-{admission_year}-{program_code.upper()}-{count:04d}"


@transaction.atomic
def create_student(validated_data):
    """
    Creates a User + Student record atomically.
    Generates a real roll/registration number and sends credentials via email.
    """
    temp_password = generate_temporary_password()
    email = validated_data["email"]
    admission_year = datetime.now().year

    user = User.objects.create_user(
        username=email,
        email=email,
        password=temp_password,
        role="STUDENT",
        first_name=validated_data["first_name"],
        last_name=validated_data["last_name"],
        must_change_password=True,
        is_verified=True,  # Admin-created accounts are pre-verified
    )

    # Fetch program to get code for roll/reg number
    from academics.models import Program
    program = Program.objects.get(id=validated_data["program_id"])

    # Count existing students in this program+year for sequential numbering
    student_count = (
        Student.objects.filter(
            program_id=validated_data["program_id"],
            admission_year=admission_year
        ).count() + 1
    )

    roll_number = generate_roll_number(program.code, admission_year, student_count)
    registration_number = generate_registration_number(program.code, admission_year, student_count)

    student = Student.objects.create(
        user=user,
        department_id=validated_data["department_id"],
        program_id=validated_data["program_id"],
        guardian_name=validated_data["guardian_name"],
        guardian_phone=validated_data["guardian_phone"],
        emergency_contact=validated_data["emergency_contact"],
        roll_number=roll_number,
        registration_number=registration_number,
        admission_year=admission_year,
    )

    send_account_credentials_email.delay(email, temp_password, "Student")

    return student
