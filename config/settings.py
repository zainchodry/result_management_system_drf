"""
Django settings for Result Management System DRF.

Production-ready settings using python-decouple for environment variable management.
"""

from pathlib import Path
from datetime import timedelta
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ──────────────────────────────────────────────────────────────────────────────
# SECURITY
# ──────────────────────────────────────────────────────────────────────────────

SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())


# ──────────────────────────────────────────────────────────────────────────────
# INSTALLED APPS
# ──────────────────────────────────────────────────────────────────────────────

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_spectacular',
]

PROJECT_APPS = [
    'accounts',
    'students',
    'teachers',
    'academics',
    'results',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS


# ──────────────────────────────────────────────────────────────────────────────
# MIDDLEWARE
# ──────────────────────────────────────────────────────────────────────────────

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',       # Static files in production
    'corsheaders.middleware.CorsMiddleware',             # CORS headers
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'


# ──────────────────────────────────────────────────────────────────────────────
# TEMPLATES
# ──────────────────────────────────────────────────────────────────────────────

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ──────────────────────────────────────────────────────────────────────────────
# DATABASE
# ──────────────────────────────────────────────────────────────────────────────

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="result_management"),
        "USER": config("DB_USER", default="myuser"),
        "PASSWORD": config("DB_PASSWORD", default="mypassword"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}


# ──────────────────────────────────────────────────────────────────────────────
# AUTH
# ──────────────────────────────────────────────────────────────────────────────

AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ──────────────────────────────────────────────────────────────────────────────
# DJANGO REST FRAMEWORK
# ──────────────────────────────────────────────────────────────────────────────

REST_FRAMEWORK = {
    # Default authentication: JWT Bearer tokens
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # Default permission: require authentication unless overridden
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    # Schema generation
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # Throttling
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
}


# ──────────────────────────────────────────────────────────────────────────────
# JWT SETTINGS
# ──────────────────────────────────────────────────────────────────────────────

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=config('JWT_ACCESS_LIFETIME_MINUTES', default=60, cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=config('JWT_REFRESH_LIFETIME_DAYS', default=7, cast=int)),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}


# ──────────────────────────────────────────────────────────────────────────────
# DRF SPECTACULAR (Swagger / ReDoc)
# ──────────────────────────────────────────────────────────────────────────────

SPECTACULAR_SETTINGS = {
    'TITLE': 'Result Management System API',
    'DESCRIPTION': (
        'A production-ready REST API for managing university results, built with Django REST Framework. '
        'Supports role-based access for Admins, Teachers, and Students.'
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'CONTACT': {'name': 'Admin', 'email': config('EMAIL_HOST_USER', default='admin@example.com')},
    'LICENSE': {'name': 'MIT'},
    'TAGS': [
        {'name': 'Auth', 'description': 'Registration, login, OTP verification, password management'},
        {'name': 'Profile', 'description': 'User profile management'},
        {'name': 'Students', 'description': 'Student management (Admin only)'},
        {'name': 'Teachers', 'description': 'Teacher management (Admin only)'},
        {'name': 'Academics', 'description': 'Departments, programs, semesters, courses'},
        {'name': 'Results', 'description': 'Result upload, transcript, merit list'},
    ],
}


# ──────────────────────────────────────────────────────────────────────────────
# CORS
# ──────────────────────────────────────────────────────────────────────────────

CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://127.0.0.1:3000',
    cast=Csv()
)
CORS_ALLOW_CREDENTIALS = True


# ──────────────────────────────────────────────────────────────────────────────
# INTERNATIONALIZATION
# ──────────────────────────────────────────────────────────────────────────────

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ──────────────────────────────────────────────────────────────────────────────
# STATIC & MEDIA FILES
# ──────────────────────────────────────────────────────────────────────────────

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ──────────────────────────────────────────────────────────────────────────────
# CELERY
# ──────────────────────────────────────────────────────────────────────────────

CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes


# ──────────────────────────────────────────────────────────────────────────────
# EMAIL
# ──────────────────────────────────────────────────────────────────────────────

EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.smtp.EmailBackend'
)
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)


# ──────────────────────────────────────────────────────────────────────────────
# MISCELLANEOUS
# ──────────────────────────────────────────────────────────────────────────────

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
