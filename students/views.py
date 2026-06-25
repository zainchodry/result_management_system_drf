from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth import get_user_model

from .models import Student
from .serializers import (
    StudentSerializer, StudentCreateSerializer
)
from . services import *
from rest_framework.permissions import IsAuthenticated
from .permissions import (
    IsAdminRole
)

class StudentViewSet(ModelViewSet):

    queryset = Student.objects.select_related(
        "user",
        "department",
        "program",
        "current_semester"
    )

    serializer_class = StudentSerializer

    permission_classes = [
        IsAdminRole
    ]

from rest_framework.views import APIView


class StudentSearchAPIView(APIView):

    def get(self, request):

        roll_number = request.GET.get(
            "roll_number"
        )

        try:

            student = Student.objects.get(
                roll_number=roll_number
            )

        except Student.DoesNotExist:

            return Response(
                {
                    "error":
                    "Student not found"
                },
                status=404
            )

        serializer = StudentSerializer(
            student
        )

        return Response(
            serializer.data
        )
    
class StudentDashboardAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        student = request.user.student

        return Response(
            {
                "name":
                request.user.get_full_name(),

                "roll_number":
                student.roll_number,

                "semester":
                student.current_semester.semester_no,

                "program":
                student.program.name,

                "department":
                student.department.name
            }
        )
    
class CreateStudentAPIView(
    APIView
):

    permission_classes = [
        IsAdminRole
    ]

    def post(self, request):

        serializer = (
            StudentCreateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        student = create_student(
            serializer.validated_data
        )

        return Response(
            {
                "message":
                "Student created successfully",

                "student_id":
                student.id
            }
        )

