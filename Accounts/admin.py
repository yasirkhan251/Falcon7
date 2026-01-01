from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, LoginOTP, Forgotpassword

class MyUserAdmin(UserAdmin):
    # 1. Define what appears in the user list
    list_display = ('username', 'phone', 'name', 'is_admin', 'is_staff', 'is_superuser')
    
    # 2. Rebuild the detail page (excluding first_name and last_name)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'phone', 'email', 'profile')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'doj')}),
        ('System Info', {'fields': ('server_id',)}),
    )

    # 3. Handle the user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone', 'name', 'password', 'is_admin'),
        }),
    )
    
    # Make server_id read-only in the admin so it isn't edited manually
    readonly_fields = ('server_id', 'last_login', 'date_joined')

admin.site.register(MyUser, MyUserAdmin)



@admin.register(LoginOTP)
class LoginOTPAdmin(admin.ModelAdmin):
    list_display = ("phone", "otp", "created_at")
    search_fields = ("phone",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(Forgotpassword)
class ForgotpasswordAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "created_at", "expires_at")
    search_fields = ("user__phone",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
