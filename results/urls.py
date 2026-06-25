from django.urls import path

from .views import (
    UploadResultAPIView,
    ResultByRollNumberAPIView,
    TranscriptAPIView,
    MeritListAPIView,
    PublishResultAPIView,
    LockResultAPIView,
    StudentResultSummaryAPIView,
)

urlpatterns = [
    path("upload/", UploadResultAPIView.as_view(), name="result-upload"),
    path("search/", ResultByRollNumberAPIView.as_view(), name="result-by-roll-number"),
    path("transcript/", TranscriptAPIView.as_view(), name="my-transcript"),
    path("merit-list/", MeritListAPIView.as_view(), name="merit-list"),
    path("publish/<int:semester_id>/", PublishResultAPIView.as_view(), name="result-publish"),
    path("lock/<int:semester_id>/", LockResultAPIView.as_view(), name="result-lock"),
    path("student/<int:student_id>/", StudentResultSummaryAPIView.as_view(), name="student-result-summary"),
]