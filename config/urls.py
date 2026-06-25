from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Token endpoints
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Application APIs
    path('api/accounts/', include('accounts.urls')),
    path('api/students/', include('students.urls')),
    path('api/teachers/', include('teachers.urls')),
    path('api/academics/', include('academics.urls')),
    path('api/results/', include('results.urls')),

    # API Schema & Documentation (drf-spectacular)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
