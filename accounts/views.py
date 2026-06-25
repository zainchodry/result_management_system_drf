from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from .models import User, PasswordResetOtp, Profile
from .serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    VerifyOTPSerializer,
    ForgetPasswordSerializer,
    ResetPasswordSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
)
from .utils import generate_otp, otp_expiry_time, get_tokens_for_user
from .tasks import send_otp_email


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        otp = generate_otp()
        PasswordResetOtp.objects.create(
            user=user,
            otp=otp,
            purpose="VERIFY",
            expires_at=otp_expiry_time()
        )
        send_otp_email.delay(user.email, otp, "VERIFY")

        return Response(
            {"message": "Account created successfully. Please check your email for the verification OTP."},
            status=status.HTTP_201_CREATED
        )


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        if not user.is_verified:
            return Response(
                {"error": "Please verify your email before logging in."},
                status=status.HTTP_403_FORBIDDEN
            )

        if user.must_change_password:
            return Response(
                {
                    "must_change_password": True,
                    "message": "You must change your temporary password before continuing.",
                },
                status=status.HTTP_200_OK
            )

        tokens = get_tokens_for_user(user)

        return Response(
            {
                "user_id": user.id,
                "email": user.email,
                "role": user.role,
                "tokens": tokens,
            },
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Logged out successfully."},
                status=status.HTTP_200_OK  # Fixed: was 201
            )
        except (TokenError, InvalidToken):
            return Response(
                {"error": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            instance=request.user,
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()  # calls update(instance, validated_data)
        return Response(
            {"message": "Password changed successfully."},
            status=status.HTTP_200_OK
        )


class VerifyEmailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:  # Fixed: was not caught
            return Response(
                {"error": "No account found with this email address."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            otp_obj = PasswordResetOtp.objects.filter(
                user=user, otp=otp, purpose="VERIFY", is_used=False
            ).latest("created_at")
        except PasswordResetOtp.DoesNotExist:
            return Response(
                {"error": "Invalid OTP."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if otp_obj.expires_at < timezone.now():
            return Response(
                {"error": "OTP has expired. Please request a new one."},
                status=status.HTTP_400_BAD_REQUEST
            )

        otp_obj.is_used = True
        otp_obj.save()
        user.is_verified = True
        user.save()

        return Response(
            {"message": "Email verified successfully. You may now log in."},
            status=status.HTTP_200_OK
        )


class ForgotPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data["email"])
        except User.DoesNotExist:  # Fixed: was not caught
            # Return 200 to avoid email enumeration attacks
            return Response(
                {"message": "If an account with this email exists, an OTP has been sent."},
                status=status.HTTP_200_OK
            )

        otp = generate_otp()
        PasswordResetOtp.objects.create(
            user=user,
            otp=otp,
            purpose="RESET",
            expires_at=otp_expiry_time()
        )
        send_otp_email.delay(user.email, otp, "RESET")

        return Response(
            {"message": "If an account with this email exists, an OTP has been sent."},
            status=status.HTTP_200_OK
        )


class VerifyResetOTPAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:  # Fixed: was not caught
            return Response(
                {"error": "No account found with this email address."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            otp_obj = PasswordResetOtp.objects.filter(
                user=user, otp=otp, purpose="RESET", is_used=False
            ).latest("created_at")
        except PasswordResetOtp.DoesNotExist:
            return Response(
                {"error": "Invalid OTP."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if otp_obj.expires_at < timezone.now():
            return Response(
                {"error": "OTP has expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "OTP verified. You may now reset your password."},
            status=status.HTTP_200_OK
        )


class ResetPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:  # Fixed: was not caught
            return Response(
                {"error": "No account found with this email address."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            otp_obj = PasswordResetOtp.objects.filter(
                user=user, otp=otp, purpose="RESET", is_used=False
            ).latest("created_at")
        except PasswordResetOtp.DoesNotExist:
            return Response(
                {"error": "Invalid OTP."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if otp_obj.expires_at < timezone.now():
            return Response(
                {"error": "OTP has expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        otp_obj.is_used = True
        otp_obj.save()

        return Response(
            {"message": "Password reset successfully. You may now log in."},
            status=status.HTTP_200_OK
        )


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get the authenticated user's profile."""
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """Update the authenticated user's profile."""
        profile, _ = Profile.objects.get_or_create(user=request.user)
        # Fixed: must pass instance so serializer calls update() not create()
        serializer = UpdateProfileSerializer(
            instance=profile,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Profile updated successfully.", "data": serializer.data},
            status=status.HTTP_200_OK
        )