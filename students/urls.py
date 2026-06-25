from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    StudentViewSet,
    StudentSearchAPIView,
    StudentDashboardAPIView,
    CreateStudentAPIView
)

router = DefaultRouter()

router.register(
    "",
    StudentViewSet,
    basename="students"
)

urlpatterns = router.urls

urlpatterns += [

    path(
        "search/",
        StudentSearchAPIView.as_view()
    ),

    path(
        "dashboard/",
        StudentDashboardAPIView.as_view()
    ),
    path("create_student", CreateStudentAPIView)
]
