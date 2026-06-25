import random
import secrets
import string
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken

def generate_otp():
    return str(random.randint(100000, 999999))

def otp_expiry_time():
    return timezone.now() + timedelta(minutes=10)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh":str(refresh),
        "access":str(refresh.access_token)
    }

def generate_temporary_password(length=10):

    chars = (
        string.ascii_letters
        + string.digits
        + "@#$%&!"
    )

    return "".join(
        secrets.choice(chars)
        for _ in range(length)
    )

