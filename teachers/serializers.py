from rest_framework import serializers
from .models import Teacher

class TeacherSerializer(
    serializers.ModelSerializer
):

    full_name = serializers.CharField(
        source="user.get_full_name",
        read_only=True
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    class Meta:

        model = Teacher

        fields = "__all__"

class TeacherCreateSerializer(
    serializers.Serializer
):

    first_name = serializers.CharField()

    last_name = serializers.CharField()

    email = serializers.EmailField()

    department_id = serializers.IntegerField()

    designation = serializers.CharField()

    joining_date = serializers.DateField()

