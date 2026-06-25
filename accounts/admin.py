from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PasswordResetOtp, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'role', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('role', 'is_verified', 'is_active', 'must_change_password')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('role', 'phone_number', 'is_verified', 'must_change_password')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('email', 'role', 'phone_number')
        }),
    )


@admin.register(PasswordResetOtp)
class PasswordResetOtpAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'purpose', 'is_used', 'expires_at', 'created_at')
    list_filter = ('purpose', 'is_used')
    search_fields = ('user__email',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'city', 'country')
    search_fields = ('user__email', 'user__username')
    list_filter = ('gender',)
