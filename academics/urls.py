from rest_framework.routers import (
    DefaultRouter
)

from .views import (
    DepartmentViewSet,
    ProgramViewSet,
    SemesterViewSet,
    CourseViewSet,
    TeacherCourseAssignmentViewSet
)

router = DefaultRouter()

router.register(
    "departments",
    DepartmentViewSet
)

router.register(
    "programs",
    ProgramViewSet
)

router.register(
    "semesters",
    SemesterViewSet
)

router.register(
    "courses",
    CourseViewSet
)

router.register(
    "teacher-assignments",
    TeacherCourseAssignmentViewSet
)

urlpatterns = router.urls

