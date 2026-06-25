from rest_framework import serializers

from .models import ResultItem, SemesterResult, GradeScale


class GradeScaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = GradeScale
        fields = "__all__"


class ResultUploadSerializer(serializers.Serializer):

    student_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    total_marks = serializers.IntegerField(min_value=1)
    obtained_marks = serializers.IntegerField(min_value=0)

    def validate(self, attrs):
        if attrs["obtained_marks"] > attrs["total_marks"]:
            raise serializers.ValidationError(
                {"obtained_marks": "Obtained marks cannot exceed total marks."}
            )
        return attrs


class ResultItemSerializer(serializers.ModelSerializer):

    course_code = serializers.CharField(source="course.course_code", read_only=True)
    course_name = serializers.CharField(source="course.course_title", read_only=True)
    credit_hours = serializers.IntegerField(source="course.credit_hours", read_only=True)
    teacher_name = serializers.SerializerMethodField()

    class Meta:
        model = ResultItem
        fields = [
            "id",
            "course_code",
            "course_name",
            "credit_hours",
            "teacher_name",
            "total_marks",
            "obtained_marks",
            "percentage",
            "grade",
            "grade_points",
            "is_passed",
        ]

    def get_teacher_name(self, obj):
        if obj.teacher:
            return obj.teacher.user.get_full_name()
        return None


class SemesterResultSerializer(serializers.ModelSerializer):

    subjects = ResultItemSerializer(many=True, read_only=True)
    semester_title = serializers.CharField(source="semester.title", read_only=True)
    semester_no = serializers.IntegerField(source="semester.semester_no", read_only=True)

    class Meta:
        model = SemesterResult
        fields = [
            "id",
            "semester_title",
            "semester_no",
            "gpa",
            "cgpa",
            "total_credit_hours",
            "earned_credit_hours",
            "is_published",
            "is_locked",
            "subjects",
        ]