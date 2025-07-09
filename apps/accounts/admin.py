from django.contrib import admin
from apps.accounts.models import CustomUser
from django.contrib.auth import get_user_model

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ('uid',)
    list_display = (
        "uid", 
        "email", 
        "first_name", 
        "last_name", 
        "status",
        "is_premium",
        "is_email_verified",
        "created_on", 
        "updated_on", 
        "is_active", 
        "is_staff", 
        "is_superuser"
    )
    list_filter = (
        'created_on', 
        'updated_on', 
        'is_premium', 
        'is_email_verified', 
        'status',
        'is_active',
        'is_staff'
    )
    fieldsets = (
        (None, {
            'fields': (
                'email', 
                'username', 
                'password', 
                'uid', 
                'first_name', 
                'last_name', 
                'firebase_token'
            )
        }),
        ('Status & Preferences', {
            'fields': (
                'status', 
                'is_premium', 
                'is_email_verified'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff', 
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': (
                'created_on', 
                'updated_on', 
                'last_login'
            )
        }),
    )
    readonly_fields = ['created_on', "updated_on", 'last_login']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 
                'password1', 
                'password2', 
                'first_name',
                'last_name',
                'is_staff', 
                'is_active',
                'is_premium'
            )
        }),
    )

    search_fields = ['uid', 'email', 'first_name', 'last_name']
    
    # Custom actions for music app
    actions = ['make_premium', 'make_regular', 'verify_email']
    
    def make_premium(self, request, queryset):
        queryset.update(is_premium=True)
        self.message_user(request, f"{queryset.count()} users marked as premium.")
    make_premium.short_description = "Mark selected users as premium"
    
    def make_regular(self, request, queryset):
        queryset.update(is_premium=False)
        self.message_user(request, f"{queryset.count()} users marked as regular.")
    make_regular.short_description = "Mark selected users as regular"
    
    def verify_email(self, request, queryset):
        queryset.update(is_email_verified=True)
        self.message_user(request, f"{queryset.count()} users' emails verified.")
    verify_email.short_description = "Verify selected users' emails"

admin.site.register(CustomUser, CustomUserAdmin)
