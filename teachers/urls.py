from django.urls import path

from rest_framework.routers import (
    DefaultRouter
)

from .views import (
    TeacherViewSet,
    CreateTeacherAPIView,
    TeacherDashboardAPIView,
    AssignedCoursesAPIView
)

router = DefaultRouter()

router.register(
    "",
    TeacherViewSet,
    basename="teachers"
)

urlpatterns = router.urls

urlpatterns += [

    path(
        "create/",
        CreateTeacherAPIView.as_view()
    ),

    path(
        "dashboard/",
        TeacherDashboardAPIView.as_view()
    ),

    path(
        "assigned-courses/",
        AssignedCoursesAPIView.as_view()
    ),
]
