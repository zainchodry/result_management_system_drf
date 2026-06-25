from decimal import Decimal

from .models import GradeScale

def calculate_grade(
    percentage
):

    grade = GradeScale.objects.filter(
        min_percentage__lte=percentage,
        max_percentage__gte=percentage
    ).first()

    return grade

def calculate_gpa(
    semester_result
):

    total_quality_points = 0

    total_credit_hours = 0

    for item in semester_result.subjects.all():

        credit_hours = (
            item.course.credit_hours
        )

        total_quality_points += (
            float(item.grade_points)
            * credit_hours
        )

        total_credit_hours += credit_hours

    if total_credit_hours == 0:
        return 0

    return round(
        total_quality_points /
        total_credit_hours,
        2
    )

def calculate_cgpa(
    student
):

    semester_results = (
        student.semester_results.all()
    )

    total = 0

    count = 0

    for result in semester_results:

        total += float(result.gpa)

        count += 1

    if count == 0:
        return 0

    return round(
        total / count,
        2
    )

