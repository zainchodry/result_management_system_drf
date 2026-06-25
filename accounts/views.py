from django.shortcuts import render
from rest_framework import generics, permissions, status
from . models import *
from . serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from . utils import *
from . tasks import *


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializers = RegisterSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            user = serializers.save()
            otp = generate_otp()
            PasswordResetOtp.objects.create(
               user = user,
               otp = otp,
               purpose = "VERIFY",
               expires_at = otp_expiry_time() 
            )
            send_otp_email.delay(
                user.email,
                otp,
                "VERIFY"
            )
            return Response(
            {
                "message":
                "Account created successfully. OTP sent."
            },
            status=status.HTTP_201_CREATED
        )
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token is None:
                return Response({"data":"Refresh Token Is Must Be Required"}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"data":"Logout Successfully"}, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        except (TokenError, InvalidToken):

            return Response({"error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializers = ChangePasswordSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(APIView):

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data["user"]
        
        if user.must_change_password:
            return Response(
                {
                    "must_change_password":
                    True,

                    "message":
                    "Please change your password before continuing."
                },
                status=200
            )
        
        if not user.is_verified:
            return Response(
                {"data":"Please Verify Your Email First"},
                status=400
            )

        tokens = get_tokens_for_user(user)

        return Response(
            {
                "user_id": user.id,
                "email": user.email,
                "role": user.role,
                "tokens": tokens
            }
        )
    
class VerifyEmailAPIView(APIView):

    def post(self, request):

        serializer = VerifyOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        try:

            user = User.objects.get(
                email=email
            )

            otp_obj = PasswordResetOtp.objects.filter(
                user=user,
                otp=otp,
                purpose="VERIFY",
                is_used=False
            ).latest("created_at")

        except PasswordResetOtp.DoesNotExist:

            return Response(
                {"error": "Invalid OTP"},
                status=400
            )

        if otp_obj.expires_at < timezone.now():

            return Response(
                {"error": "OTP expired"},
                status=400
            )

        otp_obj.is_used = True
        otp_obj.save()

        user.is_verified = True
        user.save()

        return Response(
            {
                "message":
                "Account verified successfully"
            }
        )
    
class ForgotPasswordAPIView(APIView):

    def post(self, request):

        serializer = ForgetPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = User.objects.get(
            email=serializer.validated_data["email"]
        )

        otp = generate_otp()

        PasswordResetOtp.objects.create(
            user=user,
            otp=otp,
            purpose="RESET",
            expires_at=otp_expiry_time()
        )

        send_otp_email.delay(
            user.email,
            otp,
            "RESET"
        )

        return Response(
            {
                "message":
                "OTP sent successfully"
            }
        )
    
class ResetPasswordAPIView(APIView):

    def post(self, request):

        serializer = ResetPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        user = User.objects.get(
            email=email
        )

        otp_obj = PasswordResetOtp.objects.filter(
            user=user,
            otp=otp,
            purpose="RESET",
            is_used=False
        ).latest("created_at")

        if otp_obj.expires_at < timezone.now():

            return Response(
                {
                    "error":
                    "OTP expired"
                },
                status=400
            )

        user.set_password(
            serializer.validated_data["new_password"]
        )

        user.save()

        otp_obj.is_used = True
        otp_obj.save()

        return Response(
            {
                "message":
                "Password reset successfully"
            }
        )
    
class VerifyResetOTPAPIView(APIView):

    def post(self, request):

        serializer = VerifyOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        try:

            user = User.objects.get(
                email=email
            )

            otp_obj = PasswordResetOtp.objects.filter(
                user=user,
                otp=otp,
                purpose="RESET",
                is_used=False
            ).latest("created_at")

        except PasswordResetOtp.DoesNotExist:

            return Response(
                {
                    "error":
                    "Invalid OTP"
                },
                status=400
            )

        if otp_obj.expires_at < timezone.now():

            return Response(
                {
                    "error":
                    "OTP expired"
                },
                status=400
            )

        return Response(
            {
                "message":
                "OTP verified"
            }
        )
    
class ProfileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        serializers = UpdateProfileSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    