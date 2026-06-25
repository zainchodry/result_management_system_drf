from rest_framework.viewsets import (
    ModelViewSet
)

from .models import (
    Department,
    Program,
    Semester,
    Course,
    TeacherCourseAssignment
)

from .serializers import (
    DepartmentSerializer,
    ProgramSerializer,
    SemesterSerializer,
    CourseSerializer,
    TeacherCourseAssignmentSerializer
)

from .permissions import (
    IsAdminRole
)

class DepartmentViewSet(
    ModelViewSet
):

    queryset = Department.objects.all()

    serializer_class = (
        DepartmentSerializer
    )

    permission_classes = [
        IsAdminRole
    ]

class ProgramViewSet(
    ModelViewSet
):

    queryset = Program.objects.all()

    serializer_class = (
        ProgramSerializer
    )

    permission_classes = [
        IsAdminRole
    ]

class SemesterViewSet(
    ModelViewSet
):

    queryset = Semester.objects.all()

    serializer_class = (
        SemesterSerializer
    )

    permission_classes = [
        IsAdminRole
    ]

class CourseViewSet(
    ModelViewSet
):

    queryset = Course.objects.all()

    serializer_class = (
        CourseSerializer
    )

    permission_classes = [
        IsAdminRole
    ]

class TeacherCourseAssignmentViewSet(
    ModelViewSet
):

    queryset = (
        TeacherCourseAssignment
        .objects
        .select_related(
            "teacher",
            "course",
            "semester"
        )
    )

    serializer_class = (
        TeacherCourseAssignmentSerializer
    )

    permission_classes = [
        IsAdminRole
    ]

