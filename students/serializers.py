from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(
        source="user.get_full_name",
        read_only=True
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    class Meta:

        model = Student

        fields = "__all__"


class StudentCreateSerializer(serializers.Serializer):

    first_name = serializers.CharField()

    last_name = serializers.CharField()

    email = serializers.EmailField()

    department_id = serializers.IntegerField()

    program_id = serializers.IntegerField()

    guardian_name = serializers.CharField()

    guardian_phone = serializers.CharField()

    emergency_contact = serializers.CharField()

