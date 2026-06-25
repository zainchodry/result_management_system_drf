from django.urls import path
from . views import *

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('forget-password/', ForgotPasswordAPIView.as_view(), name='forget-password'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('verify-reset-otp/', VerifyResetOTPAPIView.as_view(), name='verify-reset-otp'),
    path('profile/', ProfileView.as_view(), name='profile')
]
