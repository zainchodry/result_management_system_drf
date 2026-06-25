from rest_framework import serializers
from . models import *
from django.contrib.auth import get_user_model, password_validation, authenticate

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confitm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'phone_number', 'password', 'confirm_password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email Already Exists")
        
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Password IS Not Matched")
        
        return attrs
    
    def validate_username(self, value):
        words = value.split()

        for word in words:
            if not word[0].isupper():
                raise serializers.ValidationError("Each word must start with a capital letter.")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')

        user = User.objects.create_user(**validated_data, password=password)
        user.save()
        return user
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError("Incorrect Password")
        
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Password IS InCorrect.")
        
        password_validation.validate_password(attrs['new_password'], user)

        return attrs
    
    def create(self, validated_data):
        user = self.context['request'].user
        user.set_password(validated_data['new_password'])
        user.must_change_password = False
        user.save()
        return user
    

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField()
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    role = serializers.CharField(
        source="user.role",
        read_only=True
    )

    class Meta:
        model = Profile

        fields = [
            "email",
            "username",
            "role",
            "profile_picture",
            "gender",
            "date_of_birth",
            "address",
            "city",
            "country",
            "bio"
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

        user = authenticate(
            email=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid credentials."
            )

        attrs["user"] = user

        return attrs
    
class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()

    otp = serializers.CharField(max_length=6)