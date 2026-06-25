from rest_framework import serializers

from .models import (
    Department,
    Program,
    Semester,
    Course,
    SemesterCourse,
    TeacherCourseAssignment
)

class DepartmentSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Department
        fields = "__all__"

class ProgramSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Program
        fields = "__all__"

class SemesterSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Semester
        fields = "__all__"

class CourseSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Course
        fields = "__all__"

class TeacherCourseAssignmentSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = TeacherCourseAssignment
        fields = "__all__"

