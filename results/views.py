from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from students.models import Student
from academics.models import Course
from .permissions import IsTeacherRole, IsAdminRole
from .models import SemesterResult, ResultItem, ResultPublication
from .serializers import (
    ResultUploadSerializer,
    SemesterResultSerializer,
    GradeScaleSerializer,
)
from .services import calculate_grade, calculate_gpa, calculate_cgpa
from accounts.models import User


class UploadResultAPIView(APIView):

    permission_classes = [IsAuthenticated, IsTeacherRole]

    def post(self, request):
        serializer = ResultUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Fixed: wrap teacher access in try/except
        try:
            teacher = request.user.teacher
        except Exception:
            return Response(
                {"error": "No teacher profile is associated with this account."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            student = Student.objects.get(id=serializer.validated_data["student_id"])
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            course = Course.objects.get(id=serializer.validated_data["course_id"])
        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not student.current_semester:
            return Response(
                {"error": "Student does not have a current semester assigned."},
                status=status.HTTP_400_BAD_REQUEST
            )

        obtained_marks = serializer.validated_data["obtained_marks"]
        total_marks = serializer.validated_data["total_marks"]

        if obtained_marks > total_marks:
            return Response(
                {"error": "Obtained marks cannot exceed total marks."},
                status=status.HTTP_400_BAD_REQUEST
            )

        semester_result, _ = SemesterResult.objects.get_or_create(
            student=student,
            semester=student.current_semester
        )

        if semester_result.is_locked:
            return Response(
                {"error": "This semester's results are locked and cannot be modified."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if result already submitted for this course
        if ResultItem.objects.filter(
            semester_result=semester_result, course=course
        ).exists():
            return Response(
                {"error": "Result for this course has already been uploaded."},
                status=status.HTTP_400_BAD_REQUEST
            )

        percentage = (obtained_marks / total_marks) * 100
        grade_scale = calculate_grade(percentage)

        if not grade_scale:
            return Response(
                {"error": "No grade scale found for this percentage. Please configure grade scales first."},
                status=status.HTTP_400_BAD_REQUEST
            )

        ResultItem.objects.create(
            semester_result=semester_result,
            course=course,
            teacher=teacher,
            total_marks=total_marks,
            obtained_marks=obtained_marks,
            percentage=round(percentage, 2),
            grade=grade_scale.grade,
            grade_points=grade_scale.grade_points,
            is_passed=percentage >= 50
        )

        semester_result.gpa = calculate_gpa(semester_result)
        semester_result.save()

        # Recalculate student CGPA
        student.cgpa = calculate_cgpa(student)
        student.save()

        return Response(
            {"message": "Result uploaded successfully."},
            status=status.HTTP_201_CREATED
        )


class ResultByRollNumberAPIView(APIView):
    """Public endpoint to look up a student's published results by roll number."""

    def get(self, request):
        roll_number = request.GET.get("roll_number")
        if not roll_number:
            return Response(
                {"error": "roll_number query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            student = Student.objects.get(roll_number=roll_number)
        except Student.DoesNotExist:
            return Response(
                {"error": "No student found with this roll number."},
                status=status.HTTP_404_NOT_FOUND
            )

        results = SemesterResult.objects.filter(student=student, is_published=True)
        serializer = SemesterResultSerializer(results, many=True)

        return Response(
            {
                "student": student.user.get_full_name(),
                "roll_number": student.roll_number,
                "cgpa": student.cgpa,
                "results": serializer.data,
            }
        )


class TranscriptAPIView(APIView):
    """Student can view their own full transcript (published results only)."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student = request.user.student
        except Exception:
            return Response(
                {"error": "No student profile associated with this account."},
                status=status.HTTP_403_FORBIDDEN
            )

        results = SemesterResult.objects.filter(student=student, is_published=True)
        serializer = SemesterResultSerializer(results, many=True)

        return Response(
            {
                "student": student.user.get_full_name(),
                "roll_number": student.roll_number,
                "program": student.program.name,
                "department": student.department.name,
                "cgpa": student.cgpa,
                "results": serializer.data,
            }
        )


class MeritListAPIView(APIView):
    """Public merit list ordered by CGPA descending."""

    def get(self, request):
        students = Student.objects.filter(status="ACTIVE").order_by("-cgpa").select_related("user", "program")

        data = [
            {
                "position": idx + 1,
                "student": student.user.get_full_name(),
                "roll_number": student.roll_number,
                "program": student.program.name,
                "cgpa": student.cgpa,
            }
            for idx, student in enumerate(students)
        ]

        return Response(data)


class PublishResultAPIView(APIView):
    """Admin can publish a semester's results making them visible to students."""

    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request, semester_id):
        results = SemesterResult.objects.filter(semester_id=semester_id)
        if not results.exists():
            return Response(
                {"error": "No results found for this semester."},
                status=status.HTTP_404_NOT_FOUND
            )

        results.update(is_published=True, is_locked=True)

        ResultPublication.objects.get_or_create(
            semester_id=semester_id,
            defaults={"published_by": request.user}
        )

        return Response(
            {"message": f"Results for semester {semester_id} published successfully."},
            status=status.HTTP_200_OK
        )


class LockResultAPIView(APIView):
    """Admin can lock results to prevent further modifications."""

    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request, semester_id):
        results = SemesterResult.objects.filter(semester_id=semester_id)
        if not results.exists():
            return Response(
                {"error": "No results found for this semester."},
                status=status.HTTP_404_NOT_FOUND
            )
        results.update(is_locked=True)
        return Response(
            {"message": f"Results for semester {semester_id} locked successfully."},
            status=status.HTTP_200_OK
        )


class StudentResultSummaryAPIView(APIView):
    """Admin/Teacher can view a detailed result summary for a specific student."""

    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        try:
            student = Student.objects.select_related("user", "program", "department").get(id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        results = SemesterResult.objects.filter(student=student).prefetch_related("subjects__course")
        serializer = SemesterResultSerializer(results, many=True)

        return Response(
            {
                "student": student.user.get_full_name(),
                "roll_number": student.roll_number,
                "program": student.program.name,
                "department": student.department.name,
                "cgpa": student.cgpa,
                "results": serializer.data,
            }
        )
