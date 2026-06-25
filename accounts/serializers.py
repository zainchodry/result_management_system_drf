from rest_framework import serializers
from .models import User, PasswordResetOtp, Profile
from django.contrib.auth import password_validation, authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)  # Fixed typo: confitm_password -> confirm_password

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'phone_number', 'password', 'confirm_password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email Already Exists")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def validate_username(self, value):
        words = value.split()
        for word in words:
            if not word[0].isupper():
                raise serializers.ValidationError("Each word must start with a capital letter.")
        return value

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password": "Incorrect current password."})

        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New passwords do not match."})

        password_validation.validate_password(attrs['new_password'], user)
        return attrs

    def update(self, instance, validated_data):
        """Renamed from create() to update() — Serializer.save() calls update() when instance is provided."""
        instance.set_password(validated_data['new_password'])
        instance.must_change_password = False
        instance.save()
        return instance


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField()
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        password_validation.validate_password(attrs['new_password'])
        return attrs


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(source="user.email", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "email",
            "username",
            "role",
            "phone_number",
            "profile_picture",
            "gender",
            "date_of_birth",
            "address",
            "city",
            "country",
            "bio",
        ]


class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            "profile_picture",
            "gender",
            "date_of_birth",
            "address",
            "city",
            "country",
            "bio",
        ]


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active:
            raise serializers.ValidationError("This account has been deactivated.")

        attrs["user"] = user
        return attrs


class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)