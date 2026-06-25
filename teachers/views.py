from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.viewsets import (
    ModelViewSet
)
from academics.models import (
    TeacherCourseAssignment
)
from rest_framework.permissions import (
    IsAuthenticated
)

from .models import Teacher

from .serializers import (
    TeacherSerializer,
    TeacherCreateSerializer
)

from .services import (
    create_teacher
)

from students.permissions import (
    IsAdminRole
)

class TeacherViewSet(
    ModelViewSet
):

    queryset = Teacher.objects.select_related(
        "user",
        "department"
    )

    serializer_class = TeacherSerializer

    permission_classes = [
        IsAdminRole
    ]

class CreateTeacherAPIView(
    APIView
):

    permission_classes = [
        IsAdminRole
    ]

    def post(self, request):

        serializer = (
            TeacherCreateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        teacher = create_teacher(
            serializer.validated_data
        )

        return Response(
            {
                "message":
                "Teacher created successfully",

                "teacher_id":
                teacher.id
            }
        )
    
class TeacherDashboardAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        teacher = request.user.teacher

        return Response(
            {
                "name":
                request.user.get_full_name(),

                "employee_id":
                teacher.employee_id,

                "designation":
                teacher.designation,

                "department":
                teacher.department.name
            }
        )


class AssignedCoursesAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        teacher = request.user.teacher

        courses = (
            TeacherCourseAssignment
            .objects
            .filter(
                teacher=teacher
            )
        )

        data = []

        for item in courses:

            data.append(
                {
                    "course":
                    item.course.course_title,

                    "course_code":
                    item.course.course_code,

                    "semester":
                    item.semester.title,
                }
            )

        return Response(data)
    