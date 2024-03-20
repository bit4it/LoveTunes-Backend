from django.contrib import admin
from apps.accounts.models import CustomUser
from django.contrib.auth import get_user_model

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    ordering = ('uid',)
    list_display = ("uid","uuid","email","first_name","last_name", 'phone_number','created_on','updated_on','is_active','is_staff', 'is_guest', 'is_superuser')
    list_filter = ('created_on','updated_on', 'is_guest')
    fieldsets = (
        (None, {'fields': ('email','username', 'password', 'uid', 'uuid', 'first_name','last_name', 'phone_number', 'date_of_birth', 'firebase_token')}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    readonly_fields = ['created_on',"updated_on"]
    # filter_horizontal = ("admin_of_groups",)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 
                        'is_active', 
                        )}
        ),
    )

    search_fields = ['uid', 'phone_number', "first_name"]

admin.site.register(get_user_model(), CustomUserAdmin)