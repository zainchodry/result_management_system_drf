from celery import shared_task

from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_otp_email(email, otp, purpose):
    if purpose == "VERIFY":
        subject = "Account Verification OTP"
        message = f"""
        Your verification OTP is: {otp}

        This OTP will expire in 10 minutes.
        """
    
    else:
        subject = "Password Reset OTP"
        message = f"""
        Your password reset OTP is: {otp}

        This OTP will expire in 10 minutes.
        """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )




@shared_task
def send_account_credentials_email(
    email,
    password,
    role
):

    subject = "Your Account Has Been Created"

    message = f"""
Welcome to University Result Management System

Role: {role}

Email: {email}

Temporary Password:
{password}

Please login and change your password immediately.
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )